# Draw and process BNMR CCD image files

## bccd.read

Read image and header info from file. 

```python
get_data(filename,blacklevel=0,rescale_pixels=True)
get_header(filename)
```

Parameters: 

```
blacklevel:       float, value to set to black, all pixels of lower value raised to this level. Use to
                  clean up noise. 
filename:         str, path to .fits file
rescale_pixels:   bool, pixels are intrinsically asymmetric. Rescale image such that the pixels are 
                  square, interpolating pixel values with 3rd order spline. 
```

## bccd.draw

Draw images, with various transforms. 

```python
draw(filename,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,mask=None,**kwargs)
draw_2Dfit(shape,fn,*pars,levels=10,cmap='jet')
draw_contour(filename,n=5,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,**kwargs)
draw_edges(filename,blacklevel=0,sigma=1,alpha=1,cmap='Greys',rescale_pixels=True,draw_image=True,
                  mask=None,**kwargs)
draw_sobel(filename,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,**kwargs)
```

Parameters:

```
alpha:            float, image transparency. Range: [0,1].
blacklevel:       float, value to set to black, all pixels of lower value raised to this level. Use to
                  clean up noise. 
cmap:             str, color map to color the image. Ex: "Reds", "Greens", etc.
filename:         str, path to .fits file
fn:               function handle, function to draw
levels:           int, number of contour levels to draw
kwargs:           **dict, unused
mask:             tuple, exclude all pixels outside of circle from draw or calculation. (x0,y0,r)
pars:             *tuple, parameters passed to fn. 
rescale_pixels:   bool, pixels are intrinsically asymmetric. Rescale image such that the pixels are
                  square, interpolating pixel values with 3rd order spline. 
shape:            tuple, shape of the image (number of pixels x,y)
sigma:            float, standard deviation of rolling Gaussian filter, smoothing image features.
```

## bccd.detect

Detect shapes in the image. 

```python
get_circles(filename,rad_range,n=1,sigma=1,blacklevel=0,draw=True,rescale_pixels=True,**kwargs)
get_hlines(filename,sigma=1,min_length=50,min_gap=3,n=np.inf,blacklevel=0,draw=True,
                  rescale_pixels=True,**kwargs)
get_lines(filename,sigma=1,min_length=50,min_gap=3,theta=None,n=np.inf,blacklevel=0,draw=True,
                  rescale_pixels=True,**kwargs)
```

Parameters:

```
blacklevel:       float, value to set to black, all pixels of lower value raised to this level. Use to
                  clean up noise. 
filename:         str, path to .fits file
draw:             bool, if true, draw output
kwargs:           **dict, unused
min_length:       float, minimum length of lines to find, in pixels
min_gap:          float, maximum acceptable distance between line pixels which do not signify breaking
                  the line
n:                int, number of shapes to find
rad_range:        tuple, radius range to seach in (r_lo, r_hi)
rescale_pixels:   bool, pixels are intrinsically asymmetric. Rescale image such that the pixels are
                  square, interpolating pixel values with 3rd order spline. 
sigma:            float, standard deviation of rolling Gaussian filter, smoothing image features.
theta:            float, list of acceptable angles for the lines to point
```

## bccd.process

Fitting and extraction of key image features. 

```python
fit2D(filename,function,blacklevel=0,rescale_pixels=True,**fitargs)
fit_gaussian2D(filename,blacklevel=0,rescale_pixels=True,draw_output=True,nicedraw=True,**kwargs)
get_center(filename,blacklevel=0,draw=True,rescale_pixels=True,mask=None,**kwargs)
get_cm(filename,blacklevel=0,draw=True,rescale_pixels=True,mask=None,**kwargs)
get_gaussian2D_overlap(ylo,yhi,xlo,xhi,x0,y0,sx,sy,amp,theta=0)
```

Parameters:

```
blacklevel:       float, value to set to black, all pixels of lower value raised to this level. Use to
                  clean up noise. 
filename:         str, path to .fits file
fitargs:          **dict, arguments passed to curve_fit
draw:             bool, if true, draw output
draw_output:      bool, if true, draw output
nicedraw:         bool, if true, draw 10 contours with amplitude = 1
kwargs:           **dict, unused
mask:             tuple, exclude all pixels outside of circle from draw or calculation. (x0,y0,r)
rescale_pixels:   bool, pixels are intrinsically asymmetric. Rescale image such that the pixels are 
                  square, interpolating pixel values with 3rd order spline. 

amp:              float, unused in favour of normalized amplitude (present for ease of use)
sx,sy:            float, standard deviation
theta:            float, angle of rotation                  
x0,y0:            float, gaussian mean location
xlo:              function handle, lower integration bound [inner]
xlhi:             function handle, upper integration bound [inner]
ylo:              float, lower integration bound [outer]
yhi:              float, upper integration bound [outer]
```


## bccd.functions

Fitting functions. 

```python
gaussian2D(x,y,x0,y0,sigmax,sigmay,amp,theta=0)
```

Parameters:

```
amp:              float, unused in favour of normalized amplitude (present for ease of use)
sx,sy:            float, standard deviation
theta:            float, angle of rotation                  
x,y:              float, pixel location to evaluate at
x0,y0:            float, gaussian mean location
```


## bccd.misc

Miscellaneous functions.

```python
mask_data(data,mask=None)
```

Parameters:

```
data:             2D np.array, image, read from the file
mask:             tuple, exclude all pixels outside of circle from draw or calculation. (x0,y0,r)
```
   
