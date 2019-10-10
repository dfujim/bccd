# Miscellaneous functions
# Derek Fujimoto
# Oct 2019

import numpy as np
import skimage as ski

def mask_data(data,mask=None):
    """
        Mask image data
        
        data:       2D np array 
        mask:       (x,y,r) specifying center and radius of circle to mask on
    """
    
    # masking
    if mask is not None: 
        window = np.ones(data.shape)
        rr,cc = ski.draw.circle(mask[1],mask[0],mask[2],shape=data.shape)
        window[rr,cc] = 0
        data = np.ma.array(data,mask=window)
    else:
        data = np.ma.asarray(data)
    
    return data
    
