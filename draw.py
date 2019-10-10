# Functions for drawing 
# Derek Fujimoto
# July 2019

import numpy as np
import matplotlib.pyplot as plt

from ccddraw.read import get_data
from ccddraw.misc import mask_data

import skimage as ski
from skimage import filters
from skimage.feature import canny
from ccddraw import show_options

def draw(filename,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,mask=None,
         **kwargs):
    """
        Draw fits file to matplotlib figure
        
        filename:   name of fits file to read
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        alpha:      draw transparency
        cmap:       colormap
        
        Colormaps: 
            Greys
            Purples
            Yellows
            Blues
            Oranges
            Reds
            Greens
            ...
            
        https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    data = mask_data(data,mask)
    
    # draw
    plt.imshow(data,alpha=alpha,cmap=cmap+'_r',**show_options)

def draw_2Dfit(shape,fn,*pars,levels=10,cmap='jet'):
    """Draw the fit function as contours"""
    
    # get function image
    x = np.arange(shape[1])    
    y = np.arange(shape[0])    
    gauss = np.zeros((len(y),len(x)))
    for i in y:
        gauss[i-y[0],:] = fn(x,i,*pars)

    # draw image
    X,Y = np.meshgrid(x,y)
    ax = plt.gca()
    contours = ax.contour(X,Y,gauss,levels=levels,cmap=cmap)
    ax.clabel(contours,inline=True,fontsize='x-small',fmt='%g')
    return contours

def draw_contour(filename,n=5,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,**kwargs):
    """
        Draw contours of fits file to matplotlib figure
        
        filename:   name of fits file to read
        n:          number of contours to draw
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        alpha:      draw transparency
        cmap:       colormap    
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel)
    
    # draw
    X,Y = np.meshgrid(*tuple(map(np.arange,data.shape[::-1])))
    ax = plt.gca()
    ax.contour(X,Y,data,levels=n,cmap=cmap+'_r',**show_options)
    
def draw_edges(filename,blacklevel=0,sigma=1,alpha=1,cmap='Greys',
               rescale_pixels=True,draw_image=True,mask=None,**kwargs):
    """
        Draw fits file to matplotlib figure
        
        filename:   name of fits file to read
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        sigma:      Standard deviation of the Gaussian filter.
        alpha:      draw transparency
        cmap:       colormap
        draw_image: superimpose image 
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    data = mask_data(data,mask)
    
    # get edges
    data2 = np.copy(data)
    data2[data.mask] = blacklevel
    edges = canny(data2,sigma=sigma,low_threshold=0, high_threshold=1)
    
    # draw
    if draw_image:
        edges = np.ma.masked_where(~edges,edges.astype(int))
        plt.imshow(data,alpha=1,cmap='Greys_r',**show_options)
        plt.imshow(edges,alpha=1,cmap='Reds_r',**show_options)
    else:
        plt.imshow(edges.astype(int),alpha=alpha,cmap=cmap,**show_options)

def draw_sobel(filename,blacklevel=0,alpha=1,cmap='Greys',rescale_pixels=True,**kwargs):
    """
        Draw fits file to matplotlib figure
        
        filename:   name of fits file to read
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        alpha:      draw transparency
        cmap:       colormap
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    
    # draw
    plt.imshow(filters.sobel(data),alpha=alpha,cmap=cmap,**show_options)
