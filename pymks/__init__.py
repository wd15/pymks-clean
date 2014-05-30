import os


import nose
from nose.tools import nottest
from .mksRegressionModel import MKSRegressionModel
from .fastmksRegressionModel import FastMKSRegressionModel
from .fipyCHModel import FiPyCHModel
from .tools import draw_microstructure_discretization
from .elasticFEModel import ElasticFEModel
from .tools import bin


@nottest
def test():
    r"""
    Run all the doctests available.
    """
    path = os.path.split(__file__)[0]
    nose.main(argv=['-w', path, '--with-doctest'])

def _getVersion():
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__).version
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version

__version__ = _getVersion()


