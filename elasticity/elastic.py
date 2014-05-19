#!/usr/bin/env python
from optparse import OptionParser
import numpy as nm

import sys
sys.path.append('.')



from sfepy.base.base import IndexedStruct
from sfepy.discrete import (FieldVariable, Material, Integral, Function,
                            Equation, Equations, Problem)
from sfepy.discrete.fem import Mesh, Domain, Field
from sfepy.terms import Term
from sfepy.discrete.conditions import Conditions, EssentialBC
from sfepy.solvers.ls import ScipyDirect
from sfepy.solvers.nls import Newton
from sfepy.postprocess import Viewer

def shift_u_fun(ts, coors, bc=None, problem=None, shift=0.0):
    """
    Define a displacement depending on the y coordinate.
    """
    val = shift * coors[:,1]**2
    return val


usage = """%prog [options]"""
help = {
    'show' : 'show the results figure',
}

def main():
    from sfepy import data_dir

    parser = OptionParser(usage=usage, version='%prog')
    parser.add_option('-s', '--show',
                      action="store_true", dest='show',
                      default=False, help=help['show'])
    options, args = parser.parse_args()

    mesh = Mesh.from_file(data_dir + '/sfepy/meshes/2d/square_quad.mesh')
    domain = Domain('domain', mesh)

    min_x, max_x = domain.get_mesh_bounding_box()[:,0]
    eps = 1e-8 * (max_x - min_x)
    omega = domain.create_region('Omega', 'all')
    gamma1 = domain.create_region('Gamma1',
                                  'vertices in x < %.10f' % (min_x + eps),
                                  'facet')
    gamma2 = domain.create_region('Gamma2',
                                  'vertices in x > %.10f' % (max_x - eps),
                                  'facet')

    field = Field.from_args('fu', nm.float64, 'vector', omega, approx_order=2)

    u = FieldVariable('u', 'unknown', field)
    v = FieldVariable('v', 'test', field, primary_var_name='u')

    def lam_func_(ts, coors, mode=None, **kwargs):
        if mode != 'qp':
            return
        else:
            value = 100. * (coors[:, 0] > .25) + 0.01
            value.shape = (coors.shape[0], 1, 1)
            one = nm.ones_like(value)
            return {'lam' : value, 'mu' : one}

    lam_func = Function('lam_func_', lam_func_)
        
    m = Material('m', function=lam_func)
    f = Material('f', val=[[0.02], [0.01]])

    integral = Integral('i', order=3)

    t1 = Term.new('dw_lin_elastic_iso(m.lam, m.mu, v, u)',
                  integral, omega, m=m, v=v, u=u)
    t2 = Term.new('dw_volume_lvf(f.val, v)', integral, omega, f=f, v=v)
    eq = Equation('balance', t1 + t2)
    eqs = Equations([eq])

    fix_u = EssentialBC('fix_u', gamma1, {'u.all' : 0.0})

    bc_fun = Function('shift_u_fun', shift_u_fun, extra_args={'shift' : 0.01})
    shift_u = EssentialBC('shift_u', gamma2, {'u.0' : bc_fun})

    ls = ScipyDirect({})

    nls_status = IndexedStruct()
    nls = Newton({}, lin_solver=ls, status=nls_status)

    pb = Problem('elasticity', equations=eqs, nls=nls, ls=ls)
    pb.save_regions_as_groups('regions')

    pb.time_update(ebcs=Conditions([fix_u, shift_u]))

    vec = pb.solve()
    print nls_status

    pb.save_state('linear_elasticity.vtk', vec)

    if options.show:
        view = Viewer('linear_elasticity.vtk')
        view(vector_mode='warp_norm', rel_scaling=2,
             is_scalar_bar=True, is_wireframe=True)

if __name__ == '__main__':
    main()
