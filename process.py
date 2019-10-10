# Image processing
# Derek Fujimoto
# Oct 2019

import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits

from scipy.optimize import curve_fit
from scipy.integrate import dblquad

from ccddraw.read import get_data
from ccddraw.misc import mask_data
from ccddraw.functions import gaussian2D
from ccddraw.draw import draw_2Dfit
from ccddraw import show_options

def fit2D(filename,function,blacklevel=0,rescale_pixels=True,**fitargs):
    """
        Fit general function to fits file
    """
    
    # get data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    
    data = data[:300,:200]
    
    # flatten the image
    flat = np.ravel(data)
    
    # get number of fit parameters (first two are x,y)
    npar = len(function.__code__.co_varnames)-2
    if 'p0' not in fitargs:
        fitargs['p0'] = np.ones(npar)
        
    # get zero
    zero = np.min(flat)
    flat -= zero
    
    # normalize
    flat /= np.max(flat)
    
    # flatten the funtion 
    def fitfn(xy,*pars):    
        output = function(*xy,*pars)
        return np.ravel(output)
    
    # fit
    x = np.indices(data.shape)[::-1]
    return curve_fit(fitfn,x,flat,**fitargs)
    
def fit_gaussian2D(filename,blacklevel=0,rescale_pixels=True,
                   draw_output=True,nicedraw=True,**kwargs):
    """
        Fit 2D gaussian to image
    """
    
    # get data 
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    
    # estimate moments https://scipy-cookbook.readthedocs.io/items/FittingData.html
    total = data.sum()
    X, Y = np.indices(data.shape)
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = np.sqrt(np.abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(np.abs((np.arange(row.size)-x)**2*row).sum()/row.sum()) 
    
    # fit 
    p0 = (x,y,width_x,width_y,1,0)
    par,cov = fit2D(filename,gaussian2D,blacklevel=blacklevel,
                  rescale_pixels=rescale_pixels,p0=p0)
    std = np.diag(cov)**0.5
    
    # draw output
    if draw_output or nicedraw:
        plt.figure()    
        draw(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
        contours = draw_2Dfit(data.shape,gaussian2D,*par[:4],1,0,**kwargs)
        
        if nicedraw:
            plt.xlim((par[0]-4*par[2],par[0]+4*par[2]))
            plt.ylim((par[1]-4*par[3],par[1]+4*par[3]))
            plt.gca().clabel(contours,inline=True,fontsize='x-small',fmt='%g')
    
    return(par,std)
    
def get_center(filename,blacklevel=0,draw=True,rescale_pixels=True,mask=None,**kwargs):
    """
        Get image center of mass
        
        filename:   name of fits file to read
        radii:      specify raidus ranges (lo,hi)
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
        mask:       (x,y,r) specifying center and radius of circle to mask on
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    fid = fits.open(filename)[0]
    black = max(blacklevel,fid.header['BZERO'])
    
    # mask
    data = mask_data(data,mask)
        
    # compress
    sumx = np.ma.mean(data,axis=0)
    sumy = np.ma.mean(data,axis=1)
    
    # shift baseline
    sumx -= black
    sumy -= black
    
    # normalize
    normx = np.ma.max(sumx)
    normy = np.ma.max(sumy)
    
    sumx /= normx
    sumy /= normy
    
    # fit with gaussian
    gaus = lambda x,x0,sig,amp,base : amp*np.exp(-((x-x0)/(2*sig))**2)+base
    
    parx,cov = curve_fit(gaus,np.arange(len(sumx)),sumx,p0=(180,10,1,0),
                            bounds=((0,0,0,-np.inf),np.inf))
    stdx = np.diag(cov)**0.5
    
    pary,cov = curve_fit(gaus,np.arange(len(sumy)),sumy,p0=(260,10,1,0),
                            bounds=((0,0,0,-np.inf),np.inf))
    stdy = np.diag(cov)**0.5               
    
    # draw
    if draw:
        plt.figure()
        plt.plot(sumx*normx,label='x')
        plt.plot(sumy*normy,label='y')
        
        fitx = np.linspace(0,max(len(sumx),len(sumy)),5000)
        plt.plot(fitx,gaus(fitx,*parx)*normx,color='k')
        plt.plot(fitx,gaus(fitx,*pary)*normy,color='k')     
        plt.legend()
        
        plt.figure()
        plt.imshow(data,cmap='Greys_r',**show_options)
        plt.errorbar(parx[0],pary[0],xerr=2*parx[1],yerr=2*pary[1],fmt='o',
                      fillstyle='none',markersize=9)
                      
        if pary[1] > 2 and parx[1] > 2:
            plt.ylim(pary[0]-pary[1]*6,pary[0]+pary[1]*6)   
            plt.xlim(parx[0]-parx[1]*6,parx[0]+parx[1]*6)
            
    # return 
    return (parx[0],pary[0],parx[1],pary[1])

def get_cm(filename,blacklevel=0,draw=True,rescale_pixels=True,mask=None,
           **kwargs):
    """
        Get image center of mass
        
        filename:   name of fits file to read
        radii:      specify raidus ranges (lo,hi)
        blacklevel: value to set to black, all pixels of lower value raised 
                    to this level
    """
    
    # get raw data
    data = get_data(filename,blacklevel=blacklevel,rescale_pixels=rescale_pixels)
    data = mask_data(data,mask)
    
    # compress
    sumx = np.ma.mean(data,axis=0)
    sumy = np.ma.mean(data,axis=1)
    
    # estimate center with weighted average
    sumx -= np.ma.min(sumx)
    sumy -= np.ma.min(sumy)
    
    nsumx = len(sumx)
    nsumy = len(sumy)
    
    cx = np.ma.average(np.arange(nsumx),weights=sumx)
    cy = np.ma.average(np.arange(nsumy),weights=sumy)

    # draw
    if draw:
        plt.figure()
        plt.imshow(data,cmap='Greys_r',**show_options)
        plt.plot(cx,cy,'x')
            
    # return 
    return (cx,cy)

def get_gaussian2D_overlap(ylo,yhi,xlo,xhi,x0,y0,sx,sy,amp,theta=0):
    """
        Get integral of gaussian2D PDF within some interval, normalized to the 
        area such that the returned overlap is the event probability within the 
        range. 
        
        ylo:    lower integration bound [outer] (float)
        yhi:    upper integration bound [outer] (float)
        xlo:    lower integration bound [inner] (lambda function)
        xlhi:   upper integration bound [inner] (lambda function)
        x0,y0:  gaussian mean location
        sx,sy:  standard deviation
        amp:    unused in favour of normalized amplitude (present for ease of use)
        theta:  angle of rotation
        
            integration is: 
                
                int_y int_x G(x,y) dx dy
        
        
        returns overlap as given by dblquad
    """
    
    # get normalized amplitude
    # https://en.wikipedia.org/wiki/Gaussian_function
    a = 0.5*(np.cos(theta)/sx)**2 + 0.5*(np.sin(theta)/sy)**2
    b = 0.25*-(np.sin(theta)/sx)**2 + 0.25*(np.sin(theta)/sy)**2
    c = 0.5*(np.sin(theta)/sx)**2 + 0.5*(np.cos(theta)/sy)**2
    amp = np.sqrt(a*c-b**2)/np.pi
    
    # make PDF
    gaus = lambda x,y: gaussian2D(x,y,x0,y0,sx,sy,amp,theta)
    
    # integrate: fraction of beam overlap
    return dblquad(gaus,ylo,yhi,xlo,xhi)[0]
    
    

