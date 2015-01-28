"""Convolution Kernels

:author: David Huard <david.huard@gmail.com>

The use of hanning ripples for animating lic images is suggested in 
Cabral and Leedom (1993). 

"""
__all__ = ['hanning_ripples']
import numpy as np

hanning = np.hanning

def __hanning_window(x):
    """Return the value of the hanning function.
    
    One cycle correspongs to the domain [0,1]. 
    """
    x = np.array(x)
    return 0.5-0.5*np.cos(2.0*np.pi*x)


def hanning_ripples(N=31, shift=0, ripples=3):
    """Return a kernel composed of an hanning enveloppe superposed on 
    phase shifted hanning ripples. 

    A vector field can be "animated" to provide a sense of the direction of 
    flow by creating a series of lic images, each one computed from the same
    texture, but with a sequence of kernels that are slighly phase shifted 
    with respect to each other. 
   
    
    Parameters
    ----------
    N : int
      Kernel length. 
    shift : float
      Phase shift [0,1].
    ripples : int
      Number of ripples. 
    
    Returns
    -------
    out : 1D array (N,)
      Linearly spaced kernel values. 
    """

    """
    Example (CHECK THAT IT WORKS)
    -------
    vectors = ...
    texture = ...
    images = []
    L = 10
    for i in range(L):
       kernel = hanning_ripples(shift=np.linspace(0,1,L,endpoint=False)).astype(np.float32)
       images.append(line_integral_convolution(vectors, texture, kernel)
    """

    enveloppe = hanning(N)
    signal = __hanning_window(shift+np.linspace(0,1,N)*ripples)
    return signal*enveloppe





#################################
#            TESTS              #
#################################


def test_hanning_window():
    from numpy.testing import assert_equal
    assert_equal(__hanning_window([0., .5, 1.]), [0., 1., 0.])


def test_hanning_ripples():
    from numpy.testing import assert_equal, assert_array_almost_equal
    a = hanning_ripples(N=21, ripples=1)
    b = __hanning_window(np.linspace(0,1,21))**2
    assert_array_almost_equal(a, b)

    a = hanning_ripples(N=21)
    assert_equal(a.argmax(), 10)
    b = hanning_ripples(N=21, shift=1)
    assert_array_almost_equal(a, b)



if __name__ == '__main__':
    import nose
    nose.runmodule()
    
