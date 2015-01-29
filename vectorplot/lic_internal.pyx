"""
Algorithm based on "Imaging Vecotr Fields Using Line Integral Convolution" 
                   by Brian Cabral and Leith Leedom

"""
import numpy as np
cimport numpy as np

cdef void _advance(float vx, float vy,
        int* x, int* y, float*fx, float*fy, int w, int h):
    """Move to the next pixel in the vector direction. 
    
    This function updates x, y, fx, and fy in place. 
    
    Parameters
    ----------
    vx : float
      Vector x component.     
    vy :float
      Vector y component.
    x : int
      Pixel x index. Updated in place.
    y : int
      Pixel y index. Updated in place.
    fx : float
      Position along x in the pixel unit square. Updated in place.
    fy : float
      Position along y in the pixel unit square. Updated in place.
    w : int
      Number of pixels along x.
    h : int
      Number of pixels along y.
    """
    
    cdef float tx, ty
    cdef int zeros

    zeros = 0
    
    # Think of tx (ty) as the time it takes to reach the next pixel 
    # along x (y).

    if vx>0:
        tx = (1-fx[0])/vx
    elif vx<0:
        tx = -fx[0]/vx
    else:
        zeros += 1
        tx = 1e100
    if vy>0:
        ty = (1-fy[0])/vy
    elif vy<0:
        ty = -fy[0]/vy
    else:
        zeros += 1
        ty = 1e100

    if zeros==2:
        return
    
    if tx<ty:    # We reached the next pixel along x first.
        if vx>=0:
            x[0]+=1
            fx[0]=0
        else:
            x[0]-=1
            fx[0]=1
        fy[0]+=tx*vy
    else:        # We reached the next pixel along y first.
        if vy>=0:
            y[0]+=1
            fy[0]=0
        else:
            y[0]-=1
            fy[0]=1
        fx[0]+=ty*vx
    if x[0]>=w:
        x[0]=w-1 # FIXME: other boundary conditions?
    if x[0]<0:
        x[0]=0 # FIXME: other boundary conditions?
    if y[0]<0:
        y[0]=0 # FIXME: other boundary conditions?
    if y[0]>=h:
        y[0]=h-1 # FIXME: other boundary conditions?


#np.ndarray[float, ndim=2] 
def line_integral_convolution(
        np.ndarray[float, ndim=2] u,
        np.ndarray[float, ndim=2] v,
        np.ndarray[float, ndim=2] texture,
        np.ndarray[float, ndim=1] kernel,
        polarization=False):
    """Return an image of the texture array blurred along the local 
    vector field orientation. 

    Parameters
    ----------
    u : array (ny, nx)
      Vector field x component.
    v : array (ny, nx)
      Vector field y component.
    texture : array (ny,nx)
      The texture image that will be distorted by the vector field. 
      Usually, a white noise image is recommended to display the 
      fine structure of the vector field. 
    kernel : 1D array 
      The convolution kernel: an array weighting the texture along
      the stream line. For static images, a box kernel (equal to one)
      of length max(nx,ny)/10 is appropriate. The kernel should be 
      symmetric.
    polarization : boolean
      If True, treat the vector field as a polarization (so that the
      vectors have no distinction between forward and backward).
      
    Returns
    -------
    out : array(ny,nx)
      An image of the texture convoluted along the vector field 
      streamlines. 
      
    """

    cdef int i,j,k,x,y
    cdef int h,w,kernellen
    cdef int t
    cdef float fx, fy, tx, ty
    cdef float ui, vi, last_ui, last_vi
    cdef np.ndarray[float, ndim=2] result
    cdef int pol

    if polarization:
        pol = 1
    else:
        pol = 0
    
    ny = u.shape[0]
    nx = u.shape[1]
    
    kernellen = kernel.shape[0]
 
    result = np.zeros((ny,nx),dtype=np.float32)

    for i in range(ny):
        for j in range(nx):
            x = j
            y = i
            fx = 0.5
            fy = 0.5
            last_ui = 0
            last_vi = 0
            
            k = kernellen//2
            #print i, j, k, x, y
            result[i,j] += kernel[k]*texture[y,x]

            while k<kernellen-1:
                ui = u[y,x]
                vi = v[y,x]
                if pol and (ui*last_ui+vi*last_vi)<0:
                    ui = -ui
                    vi = -vi
                last_ui = ui
                last_vi = vi
                _advance(ui,vi,
                        &x, &y, &fx, &fy, nx, ny)
                k+=1
                #print i, j, k, x, y
                result[i,j] += kernel[k]*texture[y,x]

            x = j
            y = i
            fx = 0.5
            fy = 0.5
            last_ui = 0
            last_vi = 0
   
            k = kernellen//2
   
            while k>0:
                ui = u[y,x]
                vi = v[y,x]
                if pol and (ui*last_ui+vi*last_vi)<0:
                    ui = -ui
                    vi = -vi
                last_ui = ui
                last_vi = vi
                _advance(-ui,-vi,
                        &x, &y, &fx, &fy, nx, ny)
                k-=1
                #print i, j, k, x, y
                result[i,j] += kernel[k]*texture[y,x]
                    
    return result

