import numpy as np


def test_nonperiodic_autocorrelation():
    '''
    test nonperiodic autocorrelation for spatial statistics
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import autocorrelate
    X = np.array([[[1, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]])
    basis = DiscreteIndicatorBasis(n_states=2)
    X_auto = autocorrelate(X, basis)

    X_result = np.array([[[0,       0,       0,       0],
                          [1. / 8, 1. / 12, 3. / 16, 1. / 12],
                          [0.2, 2. / 15,     0.3, 2. / 15],
                          [1. / 8, 1. / 12, 3. / 16, 1. / 12],
                          [0,       0,       0,       0]]])

    assert(np.allclose(X_result, X_auto[..., 1]))


def test_periodic_autocorrelation():
    '''
    test periodic autocorrelation for spatial statistics
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import autocorrelate
    X = np.array([[[1, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]])
    basis = DiscreteIndicatorBasis(n_states=2)
    X_auto = autocorrelate(X, basis, periodic_axes=(0, 1))

    X_result = np.array([[[0,   0,    0,   0],
                          [0.1, 0.1, 0.15, 0.1],
                          [0.2, 0.2,  0.3, 0.2],
                          [0.1, 0.1, 0.15, 0.1],
                          [0,   0,    0,   0]]])

    assert(np.allclose(X_result, X_auto[..., 1]))


def test_nonperiodic_crosscorrelation():
    '''
    test nonperiodic crosscorrelation
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import crosscorrelate
    X = np.array([[[1, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]])
    basis = DiscreteIndicatorBasis(n_states=2)
    X_cross = crosscorrelate(X, basis)

    X_result = np.array([[[1 / 3., 4 / 9., 0.5,  4 / 9., ],
                          [1 / 8., 0.25, 3 / 16., 0.25],
                          [0., 2 / 15.,  0., 2 / 15.],
                          [0., 1 / 12., 0, 1 / 12.],
                          [0,   0,    0,   0]]])
    assert(np.allclose(X_result, X_cross[..., 0]))


def test_periodic_crosscorrelation():
    '''
    test periodic crosscorrelation
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import crosscorrelate
    X = np.array([[[1, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]])
    basis = DiscreteIndicatorBasis(n_states=2)
    X_cross = crosscorrelate(X, basis, periodic_axes=(0, 1))

    X_result = np.array([[[0.3, 0.3, 0.3,  0.3],
                          [0.2, 0.2, 0.15, 0.2],
                          [0.1, 0.1,  0., 0.1],
                          [0.2, 0.2, 0.15, 0.2],
                          [0.3, 0.3, 0.3,  0.3]]])

    assert(np.allclose(X_result, X_cross[..., 0]))


def test_nonperiodic_correlate():
    '''
    test corrleate for non-periodic microstructures
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import correlate

    X = np.array([[[0, 0, 1, 0],
                   [0, 0, 1, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 0],
                   [0, 0, 1, 0]],
                  [[0, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 0],
                   [0, 1, 0, 0]]])
    basis = DiscreteIndicatorBasis(n_states=2)
    X_corr = correlate(X, basis)
    X_result = [[2 / 3.,  4 / 9.,  0.75,  4 / 9.],
                [5 / 8.,   0.5,  0.75,   0.5],
                [0.6,  7 / 15.,   0.8,  7 / 15.],
                [5 / 8.,   0.5,  0.75,   0.5],
                [0.5,  4 / 9.,  0.75,  4 / 9.]]
    assert(np.allclose(X_result, X_corr[0, ..., 0]))


def test_periodic_correlate():
    '''
    test corrleate for periodic microstructures
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import correlate

    X = np.array([[[0, 0, 1, 0],
                   [0, 0, 1, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 0],
                   [0, 0, 1, 0]],
                  [[0, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 0],
                   [0, 1, 0, 0]]])
    basis = DiscreteIndicatorBasis(n_states=2)
    X_corr = correlate(X, basis, periodic_axes=(0, 1))
    X_result = [[0.6,  0.6,  0.75,  0.6],
                [0.6,  0.6,  0.75,  0.6],
                [0.6,  0.6,   0.8,  0.6],
                [0.6,  0.6,  0.75,  0.6],
                [0.6,  0.6,  0.75,  0.6]]
    assert(np.allclose(X_result, X_corr[0, ..., 0]))


def test_periodic_mask():
    '''
    test uncertainty masks for periodic axes.
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import autocorrelate
    from pymks.datasets import make_checkerboard_microstructure

    X = make_checkerboard_microstructure(1, 3)
    basis = DiscreteIndicatorBasis(n_states=2)
    mask = np.ones((X.shape))
    mask[0, 0, 0] = 0
    X_auto_periodic_mask = autocorrelate(X, basis, periodic_axes=[0, 1],
                                         confidence_index=mask)
    X_result_0 = np.array([[[1 / 7., 1 / 7., 3 / 7.],
                          [1 / 7., 0.5, 1 / 7.],
                          [3 / 7., 1 / 7., 1 / 7.]]])
    X_result_1 = np.array([[[2 / 7., 1 / 7., 2 / 7.],
                          [1 / 7., 0.5, 1 / 7.],
                          [2 / 7., 1 / 7., 2 / 7.]]])
    X_result = np.concatenate((X_result_0[..., None],
                               X_result_1[..., None]), axis=-1)
    assert np.allclose(X_auto_periodic_mask, np.concatenate(X_result))


def test_nonperiodic_mask():
    '''
    test uncertainty masks for nonperiodic axes.
    '''
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import autocorrelate
    from pymks.datasets import make_checkerboard_microstructure

    X = make_checkerboard_microstructure(1, 3)
    basis = DiscreteIndicatorBasis(n_states=2)
    mask = np.ones((X.shape))
    mask[0, 0, 0] = 0
    X_auto_nonperiodic_mask = autocorrelate(X, basis, confidence_index=mask)
    X_result_0 = np.array([[[1 / 3., 0, 0.5],
                          [0, 0.5, 0.],
                          [0.5, 0, 1 / 3.]]])
    X_result_1 = np.array([[[2 / 3., 0, 0.5],
                          [0, 0.5, 0.],
                          [0.5, 0, 2 / 3.]]])
    X_result = np.concatenate((X_result_0[..., None],
                               X_result_1[..., None]), axis=-1)
    assert np.allclose(X_auto_nonperiodic_mask, np.concatenate(X_result))


def test_mixperdic_mask():
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import autocorrelate
    from pymks.datasets import make_checkerboard_microstructure

    X = make_checkerboard_microstructure(1, 3)
    basis = DiscreteIndicatorBasis(n_states=2)
    mask = np.ones((X.shape))
    mask[0, 0, 0] = 0
    X_auto_mixperiodic_mask = autocorrelate(X, basis, periodic_axes=[0],
                                            confidence_index=mask)
    X_result_0 = np.array([[[1 / 5., 1 / 7., 2 / 5.],
                          [0, 0.5, 0],
                          [2 / 5., 1 / 7., 1 / 5.]]])
    X_result_1 = np.array([[[2 / 5., 1 / 7., 2 / 5.],
                          [0, 0.5, 0.],
                          [2 / 5., 1 / 7., 2 / 5.]]])
    X_result = np.concatenate((X_result_0[..., None],
                               X_result_1[..., None]), axis=-1)
    assert np.allclose(X_auto_mixperiodic_mask, np.concatenate(X_result))


def test_mask_two_samples():
    from pymks import DiscreteIndicatorBasis
    from pymks.stats import correlate
    from pymks.datasets import make_microstructure

    X = make_microstructure(n_samples=2, n_phases=2, size=(3, 3),
                            grain_size=(2, 2), seed=99)
    basis = DiscreteIndicatorBasis(n_states=2)
    mask = np.ones(X.shape)
    mask[:, 0, 0] = 0.
    X_corr = correlate(X, basis, confidence_index=mask)
    X_result = np.array([[[[1 / 3., 1 / 3., 1 / 3.],
                           [1 / 5., 1 / 5., 1 / 5.],
                           [1 / 4., 1 / 4., 0]],
                          [[1 / 5., 1 / 5., 2 / 5.],
                           [1 / 2., 1 / 2., 0],
                           [1 / 5., 1 / 5., 1 / 5.]],
                          [[1 / 4., 1 / 4., 1 / 2.],
                           [1 / 5., 1 / 5., 2 / 5.],
                           [1 / 3., 1 / 3., 0]]],
                         [[[0., 0., 1 / 3.],
                           [2 / 5., 3 / 5., 0.],
                           [0., 0., 1 / 2.]],
                          [[0., 0., 2 / 5.],
                           [3 / 8., 5 / 8., 0],
                           [0., 0., 3 / 5.]],
                          [[0., 0., 1 / 2.],
                           [2 / 5., 3 / 5., 0.],
                           [0., 0., 2 / 3.]]]])
    assert np.allclose(X_corr, X_result)


def test_normalization():
    from pymks import PrimitiveBasis
    from pymks.stats import _normalize
    prim_basis = PrimitiveBasis()
    Nx = Ny = 5
    X_ = np.zeros((1, Nx, Ny, 1))
    prim_basis._axes = np.arange(X_.ndim - 2) + 1
    _Fkernel_shape = np.array((2 * Nx, Ny))
    norm = _normalize(X_, prim_basis, _Fkernel_shape, None)
    assert norm.shape == (1, Nx, Ny, 1)
    assert np.allclose(norm[0, Nx / 2, Ny / 2, 0], 25)

if __name__ == '__main__':
    test_periodic_crosscorrelation()
    test_nonperiodic_crosscorrelation()
    test_periodic_autocorrelation()
    test_nonperiodic_autocorrelation()
