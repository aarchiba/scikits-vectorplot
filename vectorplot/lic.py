import numpy as np


def lic_flow(vectors,len_pix=10):
    """Return an array describing for each pixel in the vector field
    the stream line coordinates.
    
    This function is useful to produce a sequence of the images showing
    the vectors flow direction by phase shifting the kernel.
    
    
    Parameters
    ----------
    vectors : array (m,n,2) 
      The vector fields. 
    len_pix : int
      The number of pixels of the stream line in one direction. The
      total stream line length is 2*len_pix +1. 
      
    Returns
    -------
    out : array (2*len_pix+1, m, n, 2)
      Indices of the local stream line.
    """
    vectors = np.asarray(vectors)
    m,n,two = vectors.shape
    if two!=2:
        raise ValueError

    result = np.zeros((2*len_pix+1,m,n,2),dtype=np.int32) # FIXME: int16?
    center = len_pix
    result[center,:,:,0] = np.arange(m)[:,np.newaxis]
    result[center,:,:,1] = np.arange(n)[np.newaxis,:]

    for i in range(m):
        for j in range(n):
            y = i
            x = j
            fx = 0.5
            fy = 0.5
            for k in range(len_pix):
                vx, vy = vectors[y,x]
                print x, y, vx, vy
                if vx>=0:
                    tx = (1-fx)/vx
                else:
                    tx = -fx/vx
                if vy>=0:
                    ty = (1-fy)/vy
                else:
                    ty = -fy/vy
                if tx<ty:
                    print "x step"
                    if vx>0:
                        x+=1
                        fy+=vy*tx
                        fx=0.
                    else:
                        x-=1
                        fy+=vy*tx
                        fx=1.
                else:
                    print "y step"
                    if vy>0:
                        y+=1
                        fx+=vx*ty
                        fy=0.
                    else:
                        y-=1
                        fx+=vx*ty
                        fy=1.
                if x<0: x=0
                if y<0: y=0
                if x>=n: x=n-1
                if y>=m: y=m-1
                result[center+k+1,i,j,:] = y, x



    return result
