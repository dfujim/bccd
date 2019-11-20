# Draw and process BNMR CCD image files

Object for reading and processing fits files taken by the BNMR or BNQR CCD camera.

## `bccd.fits`

Constructor: 

```python
fits(filename,rescale_pixels=True)
```

Functions: 
    
```python
detect_lines(sigma=1,min_length=50,min_gap=3,theta=None,nlines=np.inf,draw=True)
detect_hlines(sigma=1,min_length=50,min_gap=3,nlines=np.inf,draw=True,**kwargs)
detect_circles(rad_range,nlines=1,sigma=1,draw=True)
draw(black=0,alpha=1,cmap='Greys',imap=True)
draw_2Dfit(fn,*pars,levels=10,cmap='jet')
draw_contour(nlevels=5,alpha=1,cmap='Greys',imap=True)
draw_edges(sigma=1,alpha=1,cmap='Greys',imap=True) 
draw_sobel(alpha=1,cmap='Greys',imap=False)
fit2D(function,**fitargs)
fit_gaussian2D(draw=True,**fitargs)
get_center(draw=True)
get_cm(draw=True)
get_gaussian2D_overlap(ylo,yhi,xlo,xhi)
read(filename,rescale_pixels=True)
set_black(black)
set_mask(mask)
```

Data fields:

```python
black:          float, pixel value corresponding to black (zero)
data:           2D numpy array, pixel values
data_original:  numpy array, pixel values
header:         dict, header information

mask:           (x,y,r) specifying circle to mask on

result_center:      (par,names) fitting results
result_cm:          (par,names) center of mass results
result_fit2D:       (par,cov) fitting results
result_gaussian2D:  (par,cov,names) fitting results
result_gaussian2D_overlap: float, overlap
```

Some useful colourmap names:

```
    Greys
    Purples
    Yellows
    Blues
    Oranges
    Reds
    Greens
```

Parameter descriptions

```
alpha:          float, image transparency. Range: [0,1].
black:          float, value to set to black, all pixels of lower value raised to this level. Use to
                clean up noise. 

cmap:           str, color map to color the image. Ex: "Reds", "Greens", etc.
draw:           bool, if true, draw output
filename:       str, path to .fits file
fitargs:        **dict, arguments passed to curve_fit
fn:             function handle, function to draw
levels:         int, number of contour levels to draw
kwargs:         **dict, unused
mask:           tuple, exclude all pixels outside of circle from draw or calculation. (x0,y0,r)
min_length:     float, minimum length of lines to find, in pixels
min_gap:        float, maximum acceptable distance between line pixels which do not signify breaking
                the line
nlines:         int, number of shapes to find
pars:           *tuple, parameters passed to fn. 
rad_range:      tuple, radius range to seach in (r_lo, r_hi)
rescale_pixels: bool, pixels are intrinsically asymmetric. Rescale image such that the pixels are 
                square, interpolating pixel values with 3rd order spline. 
shape:          tuple, shape of the image (number of pixels x,y)
sigma:          float, standard deviation of rolling Gaussian filter, smoothing image features.
theta:          float, list of acceptable angles for the lines to point

xlo:              function handle, lower integration bound [inner]
xlhi:             function handle, upper integration bound [inner]
ylo:              float, lower integration bound [outer]
yhi:              float, upper integration bound [outer]
```



## `bccd.functions`

```python
gaussian2D(x,y,x0,y0,sigmax,sigmay,amp,theta=0)
```

Parameter descriptions

```
amp:              float, unused in favour of normalized amplitude (present for ease of use)
sx,sy:            float, standard deviation
theta:            float, angle of rotation                  
x0,y0:            float, gaussian mean location
```
