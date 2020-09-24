# Notebook tab specifying fits file object and drawing functions
# Derek Fujimoto
# Sept 2020

from tkinter import *
from tkinter import ttk, messagebox, filedialog

import os
import numpy as np
import pandas as pd

from bccd.backend.fits import fits
import bccd.backend.colors as colors
from bccd.backend.PltTracker import PltTracker as plt

# =========================================================================== # 
class fits_tab(object):
    """
        Notebook tab specifying fits file object and drawing functions
        
        Data Fields:
            
            bccd: pointer to top level
            black: StringVar, black level
            filename: name of .fits file
            img: fits image object
            style: StringVar, drawing style
            styles: dict, map drawing style to draw function
            tab_frame: tkk.Frame; top level frame for this tab
    """
    
    # ======================================================================= #
    def __init__(self, bccd, tab_frame, filename):
        
        # inputs
        self.bccd = bccd
        self.tab_frame = tab_frame
        self.filename = filename

        # read image
        img = fits(filename, plt=bccd.plt, rescale_pixels=bccd.rescale_pixels)
        self.img = img
        
        # variables
        self.black = StringVar()
        self.black.set(str(img.black))
        
        self.style = StringVar()
        self.styles = { 'Greyscale':    self.do_draw,
                        'Contours':     self.do_contour,
                        'Gradient':     self.do_sobel,
                        'Edges':        self.do_edges,
                        'Detected Circles':self.do_circles,
                        'Detected Lines':self.do_lines,
                        'Detected Horiz. Lines':self.do_hlines,            
                        }
        self.style.set(list(self.styles.keys())[0])
       
        # Column 0 -----------------------------------------------------------
        r = 0
        
        # show main header info
        ttk.Label(tab_frame,text=os.path.basename(filename)).grid(column=0,row=r,sticky=W); r+=1
        ttk.Label(tab_frame,text='Exposure: %.3f s' % img.header['EXPOSURE']).grid(column=0,row=r,sticky=W); r+=1
        
        date,time = img.header['DATE-OBS'].split('T')
        ttk.Label(tab_frame,text=date).grid(column=0,row=r,sticky=W); r+=1
        ttk.Label(tab_frame,text=time).grid(column=0,row=r,sticky=W); r+=1
        
        # black level
        frame_black = ttk.Frame(tab_frame)
        label_black = ttk.Label(frame_black,text='Black Value: ')
        entry_black = ttk.Entry(frame_black, textvariable=self.black, width=10)
        
        frame_black.grid(column=0,row=r,sticky=W); r+=1
        label_black.grid(column=0,row=0,sticky=W)
        entry_black.grid(column=1,row=0,sticky=W)
        
        frame_style = ttk.Frame(tab_frame)
        label_style = ttk.Label(frame_style,text='Draw Style: ')
        combo_style = ttk.Combobox(frame_style, textvariable=self.style, 
                                   state='readonly',width=20)
        combo_style['values'] = tuple(self.styles.keys())
        
        r += 2 
        frame_style.grid(column=0,row=r, pady=(20,0),sticky=W); r+=1
        label_style.grid(column=0,row=0,sticky=W)
        combo_style.grid(column=1,row=0,sticky=W)
        
        # Draw buttons
        frame_draw = ttk.Frame(tab_frame)
        button_draw_super = ttk.Button(frame_draw,text='Superimpose',command=self.draw_super)
        button_draw_new = ttk.Button(frame_draw,text='Draw New',command=self.draw_new)
        button_remove = ttk.Button(frame_draw,text='Remove',command=self.remove)
    
        frame_draw.grid(column=0,row=r,sticky=W); r+=1
        c = 0
        button_draw_super.grid(column=c,row=0); c+=1
        button_draw_new.grid(column=c,row=0); c+=1
        button_remove.grid(column=c,row=0); c+=1
        
        
        # Columnn 1 ----------------------------------------------------------
        button_close = ttk.Button(tab_frame,text='x',command=self.close, pad=0)
        button_close.grid(column=10,row=0,sticky=(N,E))
        
        # resizing
        tab_frame.grid_columnconfigure(9, weight=1)        # main area
        tab_frame.grid_rowconfigure(9,weight=1)            # main area

    # ======================================================================= #
    def _draw(self):
        """Draw image in current figure"""
        
        
    # ======================================================================= #
    def close(self):
        pass
    
    # ======================================================================= #
    def do_draw(self):  pass
    def do_contour(self): pass
    def do_sobel(self): pass
    def do_edges(self): pass
    def do_circles(self): pass
    def do_lines(self): pass
    def do_hlines(self): pass
    
    # ======================================================================= #
    def draw_super(self):
        """
            Draw in the active window
        """
        self._draw()
    
    # ======================================================================= #
    def draw_new(self):
        """
            Draw in a new window
        """
        plt.figure()
        self._draw()
        
    # ======================================================================= #
    def remove(self):
        pass
    
    
    
