from .abstract import _AbstractMicrostructureBasis
import numpy as np


class _ImagFFTBasis(_AbstractMicrostructureBasis):
    """This class is used to make the bases that create complex valued
    microstructure functions use the standard FFT/iFFT algorithms and selects
    the appropriate fft module depending on whether or not pyfftw is installed.
    """
    def __init__(self, *args, **kwargs):
        """
        Instance of a basis
        """
        super(_ImagFFTBasis, self).__init__(*args, **kwargs)

    def _fftn(self, X):
        """Standard FFT algorithm

        Args:
            X: NDarray (n_samples, N_x, ...)

        Returns:
            Fourier transform of X
        """
        if self._pyfftw:
            return self._fftmodule.fftn(np.ascontiguousarray(X),
                                        axes=self._axes, threads=self._n_jobs,
                                        planner_effort='FFTW_ESTIMATE',
                                        overwrite_input=True,
                                        avoid_copy=True)()
        else:
            return self._fftmodule.fftn(X, axes=self._axes)

    def _ifftn(self, X):
        """Standard iFFT algorithm

        Args:
            X: NDarray (n_samples, N_x, ...)

        Returns:
            Inverse Fourier transform of X
        """
        if self._pyfftw:
            return self._fftmodule.ifftn(np.ascontiguousarray(X),
                                         axes=self._axes, threads=self._n_jobs,
                                         planner_effort='FFTW_ESTIMATE',
                                         overwrite_input=True,
                                         avoid_copy=True)()
        else:
            return self._fftmodule.ifftn(X, axes=self._axes)

    def discretize(self, X):
        raise NotImplementedError
