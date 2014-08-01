import numpy as np


class Filter(object):
    """
    Wrapper class for convolution with a kernel and resizing of a kernel
    """
    def __init__(self, Fkernel):
        """
        Instantiate a Filter.

        Args:
          Fkernel: an array representing a convolution kernel
        """
        self.axes = np.arange(len(Fkernel.shape) - 2) + 1
        self.Fkernel = Fkernel

    def frequency2real(self):
        """
        Converts the kernel from frequency space to real space with
        the origin shifted to the center.

        Returns:
          an array in real space          
        """
        return np.real_if_close(np.fft.fftshift(np.fft.ifftn(self.Fkernel,
                                axes=self.axes), axes=self.axes))

    def real2frequency(self, kernel):
        """
        Converts a kernel from real space to frequency space.

        Args:
          kernel: an array representing a convolution kernel in real space

        Returns:
          an array in frequency space
        """
        return np.fft.fftn(np.fft.ifftshift(kernel, axes=self.axes), axes=self.axes)

    def convolve(self, X):
        """
        Convolve X with a kernel in frequency space.

        Args:
          X: array to be convolved

        Returns:
          convolution of X with the kernel
        """
        if X.shape[1:] != self.Fkernel.shape[1:]:
            raise RuntimeError("Dimensions of X are incorrect.")
        FX = np.fft.fftn(X, axes=self.axes)
        Fy = self.sum(FX * self.Fkernel)
        return np.fft.ifftn(Fy, axes=self.axes).real

    def sum(self, Fy):
        return np.sum(Fy, axis=-1)
    
    def resize(self, size):
        """
        Changes the size of the kernel to size.

        Args:
          size: tuple with the shape of the new kernel
        """
        if len(size) != len(self.Fkernel.shape[1:-1]):
            raise RuntimeError("length of resize shape is incorrect.")
        if not np.all(size >= self.Fkernel.shape[1:-1]):
            raise RuntimeError("resize shape is too small.")

        kernel = self.frequency2real()
        size = kernel.shape[:1] + size + kernel.shape[-1:]
        padsize = np.array(size) - np.array(kernel.shape)
        paddown = padsize / 2
        padup = padsize - paddown
        padarray = np.concatenate((padup[..., None],
                                   paddown[..., None]), axis=1)
        pads = tuple([tuple(p) for p in padarray])
        kernel_pad = np.pad(kernel, pads, 'constant', constant_values=0)
        Fkernel_pad = self.real2frequency(kernel_pad)

        self.Fkernel = Fkernel_pad


class Correlation(Filter):
    '''
    Computes the autocorrelation for a microstructure

    >>> n_states = 2
    >>> X = np.array([[[0, 1, 0],
    ...                [0, 1, 0],
    ... 			   [0, 1, 0]]])
    >>> from pymks.bases import DiscreteIndicatorBasis
    >>> basis = DiscreteIndicatorBasis(n_states=n_states)
    >>> X_ = basis.discretize(X)
    >>> filter_ = Correlation(X_)
    >>> X_auto = filter_.convolve(X_)
    >>> X_test = np.array([[[[1/3., 0.  ],
    ...                      [2/3., 1/3.],
    ...                      [1/3., 0.  ]],
    ...                     [[1/3., 0.  ],
    ...                      [2/3., 1/3.],
    ...                      [1/3., 0.  ]],
    ...                     [[1/3., 0.  ],
    ...                      [2/3., 1/3.],
    ...                      [1/3., 0.  ]]]])
    >>> assert(np.allclose(X_auto, X_test))

    Ags:
      X: microstructure
    Returns:
      Autocorrelations for microstructure X
    '''
    def __init__(self, kernel):
        axes = np.arange(len(kernel.shape) - 2) + 1
        Fkernel = np.conjugate(np.fft.fftn(kernel, axes=axes))
        super(Correlation, self).__init__(Fkernel)
        
    def convolve(self, X):
        X_auto = super(Correlation, self).convolve(X)
        return np.fft.fftshift(X_auto, axes=self.axes) / np.prod(X.shape[1:-1])
        
    def sum(self, Fy):
        return Fy
        
def crosscorrelate(X_):
    n_states = X_.shape[-1]
    Niter = n_states / 2 + 1
    Nslice = n_states * (n_states - 1) / 2 + n_states
    tmp = [Correlation(X_).convolve(np.roll(X_, i, axis=-1)) for i in range(Niter)]
    return np.concatenate(tmp, axis=-1)[...,:Nslice]
    
