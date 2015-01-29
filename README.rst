vectorplot: Vector Fields Visualization Algorithms
==================================================

:author: Anne Archibald 



Line Integral Convolution
-------------------------

The Line Integral Convolution (LIC) is an algorithm used to image a vector
field. Its main advantage is to show in intricate detail the fine 
structure of the vector field. It does not display the direction or 
magnitude of the vectors, although this information can be color coded 
in a postprocessing step. 


Assume we have a texture F and vector components v_x and v_y. 
The LIC algorithm is a mapping of F to F' that blurs F along the
direction of the vector. It works by computing a local streamline for
each pixel in F. Imagine that we place a particle at position (i,j) in 
the vector field, the streamline is the successive location of this 
particle forward and backward in time. The corresponding pixel in F' is 
given by the convolution of the texture along the streamline with a
user defined kernel. 
 
The result of course depends on the shape of the kernel and the length  
of the streamline. If it is too small, the texture is not sufficiently 
filtered and the motion is not clear. If it is too large, the image is 
smoothed and details of the motion are lost. For an image of size 
(256, 256), a value of 20 provides acceptable results. 


References
----------
Cabral, Brian and Laeith Leedom. Imaging vector fields using line integral
convolution. SIGGRAPH '93: Proceedings of the 20th annual conference on 
Computer graphics and interactive techniques, pages 263-270, 1993. 


