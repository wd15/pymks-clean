import os


import nose
from nose.tools import nottest
# from .mks_localization_model import MKSLocalizationModel
from .mks_localization_model import MKSLocalizationModel
from .bases.discrete import DiscreteIndicatorBasis
from .bases.legendre import LegendreBasis
from .bases.continuous import ContinuousIndicatorBasis
from .mks_homogenization_model import MKSHomogenizationModel
MKSRegressionModel = MKSLocalizationModel

@nottest
def test():
    r"""
    Run all the doctests available.
    """
    path = os.path.split(__file__)[0]
    nose.main(argv=['-w', path, '--with-doctest'])


def get_version():
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__).version
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version

__version__ = get_version()

__all__ = ['__version__',
           'test',
           'MKSLocalizationModel'
           'DiscreteIndicatorBasis',
           'ContinuousIndicatorBasis',
           'LegendreBasis',
           'MKSHomogenizationModel']
