# Read file 
# Derek Fujimoto
# Oct 2019

import os
import numpy as np
from astropy.io import fits
from skimage.transform import rescale

def get_data(filename,blacklevel=0,rescale_pixels=True):
    """
        Get xy data from fits file. Values are brightness of pixel. 
        
        filename:       name of file to open
        blacklevel:     value to set to black, all pixels of lower value raised 
                        to this level
        rescale_pixels: if True, rescale image such that pixels are square
        
        Output:     2D array of values, or list of 2D arrays
    """
    filename = os.path.join(os.getcwd(),filename)
    fid = fits.open(filename)[0]
    data = fid.data

    # fix bad pixels: set to max
    data[data<fid.header['BZERO']] = np.max(data)
    
    # clean: remove lowest values
    if blacklevel:
        data[data<blacklevel] = blacklevel
    
    # rescale image to correct pixel size asymmetry
    if rescale_pixels:
        aspect = fid.header['YPIXSZ']/fid.header['XPIXSZ']
        
        # always enlarge image, never make it smaller
        if aspect > 1:      resc = (aspect,1)
        else:               resc = (1,1/aspect)
        
        data = rescale(data,resc,order=3,multichannel=False,preserve_range=True) 
    
    return data

def get_header(filename):
    """
        Get header info as a dictionary
    """
    filename = os.path.join(os.getcwd(),filename)
    fid = fits.open(filename)[0]
    return fid.header
 
