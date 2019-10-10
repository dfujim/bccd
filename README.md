# Draw and process BNMR CCD image files

## ccddraw.read
```python
get_data(filename,blacklevel=0,rescale_pixels=True)
get_header(filename)
```

## ccddraw.draw
```python
draw(filename,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,mask=None,**kwargs)
draw_2Dfit(shape,fn,*pars,levels=10,cmap='jet')
draw_contour(filename,n=5,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,**kwargs)
draw_edges(filename,blacklevel=0,sigma=1,alpha=1,cmap='Greys',rescale_pixels=True,draw_image=True,mask=None,**kwargs)
draw_sobel(filename,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,**kwargs)
```

## ccddraw.detect
```python
get_circles(filename,rad_range,n=1,sigma=1,blacklevel=0,draw=True,rescale_pixels=True,**kwargs)
get_hlines(filename,sigma=1,min_length=50,min_gap=3,n=np.inf,blacklevel=0,draw=True,rescale_pixels=True,**kwargs)
get_lines(filename,sigma=1,min_length=50,min_gap=3,theta=None,n=np.inf,blacklevel=0,draw=True,rescale_pixels=True,**kwargs)
```

## ccddraw.process
```python
fit2D(filename,function,blacklevel=0,rescale_pixels=True,**fitargs)
fit_gaussian2D(filename,blacklevel=0,rescale_pixels=True,draw_output=True,nicedraw=True,**kwargs)
get_center(filename,blacklevel=0,draw=True,rescale_pixels=True,mask=None,**kwargs)
get_cm(filename,blacklevel=0,draw=True,rescale_pixels=True,mask=None,**kwargs)
get_gaussian2D_overlap(ylo,yhi,xlo,xhi,x0,y0,sx,sy,amp,theta=0)
```

## ccddraw.functions
```python
gaussian2D(x,y,x0,y0,sigmax,sigmay,amp,theta=0)
```

## ccddraw.misc
```python
mask_data(data,mask=None)
```
