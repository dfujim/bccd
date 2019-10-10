# Detect shapes in image 
# Derek Fujimoto
# 2019

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from skimage.feature import canny
from skimage.transform import hough_circle,hough_circle_peaks
from skimage.transform import probabilistic_hough_line

from ccddraw.read import get_data
from ccddraw.misc import mask_data
from ccddraw import show_options

def get_lines(filename,sigma=1,min_length=50,min_gap=3,theta=None,n=np.inf,
                 blacklevel=0,draw=True,rescale_pixels=True,**kwargs):
    """
        Detect lines in image
        
        filename:   name of fits file to read
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        n:          number of line s to find
        min_length: minimum length of lines to find
        min_gap:    minimum gap between pixels to avoid breaking the line    
        theta:      list of acceptable angles for the lines to point
        
        returns: list of points ((x0,y0),(x1,y1)) to identify the end points of 
                 the lines
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    
    # get edges
    edges = canny(data,sigma=sigma, low_threshold=0, high_threshold=1)
    
    # select lines
    lines = probabilistic_hough_line(edges,threshold=10,line_length=min_length,
                                     line_gap=min_gap,theta=theta)
    # draw
    if draw:
        plt.figure()
        plt.imshow(data,alpha=1,cmap='Greys_r',**show_options)
        edges = np.ma.masked_where(~edges,edges.astype(int))
        plt.imshow(edges,alpha=1,cmap='Reds_r',**show_options)
        
        for line in lines:
            plt.plot(*tuple(np.array(line).T))
            
    # return 
    return lines+2

def get_hlines(filename,sigma=1,min_length=50,min_gap=3,n=np.inf,
                 blacklevel=0,draw=True,rescale_pixels=True,**kwargs):
    """
        Detect horizontal lines in image
        
        filename:   name of fits file to read
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        n:          number of line s to find
        min_length: minimum length of lines to find
        min_gap:    minimum gap between pixels to avoid breaking the line    
        
        returns: list of y positions to identify each line
    """
    
    # make a set of ranges about pi/2
    theta = np.linspace(np.pi/2-0.01,np.pi/2+0.01,30)
    
    # get lines 
    lines = get_lines(filename=filename,sigma=sigma,min_length=min_length,
                         min_gap=min_gap,n=n,blacklevel=blacklevel,draw=draw,
                         rescale_pixels=rescale_pixels,theta=theta,**kwargs)
    
    # get y values of lines 
    return [l[0][1] for l in lines]
            
def get_circles(filename,rad_range,n=1,sigma=1,blacklevel=0,
                   draw=True,rescale_pixels=True,**kwargs):
    """
        Detect circles in image
        
        filename:   name of fits file to read
        rad_range:  specify raidus search range (lo,hi)
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        alpha:      draw transparency
        cmap:       colormap
        n:          number of circles to find
        
        returns: (center_x,center_y,radius)
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    
    # get edges
    edges = canny(data,sigma=sigma, low_threshold=0, high_threshold=1)
    
    # get radii
    hough_radii = np.arange(*rad_range, 2)
    hough_res = hough_circle(edges, hough_radii)
    
    # select cicles 
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                                total_num_peaks=n)
    
    # draw
    if draw:
        
        plt.imshow(data,alpha=1,cmap='Greys_r',**show_options)
        edges = np.ma.masked_where(~edges,edges.astype(int))
        plt.imshow(edges,alpha=1,cmap='Reds_r',**show_options)
        
        for center_y, center_x, radius in zip(cy, cx, radii):
            circle = Circle((center_x,center_y),radius,
                        facecolor='none',linewidth=1,edgecolor='g')
            plt.gca().add_patch(circle)
            
    # return 
    return (cx,cy,radii)
    
