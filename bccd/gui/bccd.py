# Draw main bccd gui
# Derek Fujimoto
# Sep 2020

from tkinter import *
from tkinter import ttk, filedialog, messagebox

# set MPL backend
import matplotlib as mpl
mpl.use('TkAgg')


import sys, os, datetime, textwrap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import weakref as wref
import webbrowser
import subprocess
import importlib
import logging

from bccd import __version__, logger_name, icon_path
import bccd.backend.colors as colors

# interactive plotting
plt.ion()

__doc__ = """

"""

# =========================================================================== #
class bccd(object):
    """
        Build the mainframe and set up the runloop for the tkinter GUI. 
        
        Data Fields:
            
            mainframe: frame for root
            notebook: notebook for adding files
    """
    
    # ======================================================================= #
    def __init__(self):
        """"""
        
        # root 
        root = Tk()
        self.root = root
        root.title("βccd: β-NMR and β-NQR Beamspot Viewer "+\
                   "(version %s)" % __version__)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # styling
        root.option_add('*tearOff', FALSE)
        root.option_add("*Font", colors.font)
        root.option_add("*Background",          colors.background)
        root.option_add("*DisabledBackground",  colors.background)
        root.option_add("*ReadonlyBackground",  colors.readonly)
        root.option_add("*Borderwidth", 2)
        
        # don't change all foregrounds or you will break the filedialog windows
        root.option_add("*Menu*Foreground",     colors.foreground)   
        root.option_add("*Spinbox*Foreground",  colors.foreground)
        root.option_add("*Listbox*Foreground",  colors.foreground)
        root.option_add("*Text*Foreground",     colors.foreground)
        
        root.option_add("*Scrollbar.Background",colors.foreground)
        
        ttk_style = ttk.Style()
        ttk_style.configure('.', font=colors.font,
                                   background=colors.background,
                                   foreground=colors.foreground,
                                   arrowcolor=colors.foreground,
                                   borderwidth=2)
                                   
        ttk_style.map('.', background=[('disabled',colors.background)],
                           fieldbackground=[('selected',colors.selected)])
                                         
        ttk_style.configure('TNotebook.Tab', padding=[50,2])
        ttk_style.configure("TNotebook.Tab",background=colors.background)
        ttk_style.map("TNotebook.Tab",background=[("selected",colors.tab)])
        
        ttk_style.configure("TEntry",foreground=colors.foreground,
                                     fieldbackground=colors.fieldbackground)
        
        ttk_style.map("TEntry",foreground     =[('active',  colors.foreground),
                                                ('disabled',colors.disabled)],
                               fieldbackground=[('active',  colors.fieldbackground),
                                                ('disabled',colors.disabled),
                                                ('readonly',colors.readonly)])
                                                                         
        ttk_style.map("TCheckbutton",foreground=[('selected',colors.selected),
                                                 ('disabled',colors.disabled)],
                                     indicatorcolor=[('selected','green3')])
        ttk_style.map('TCombobox', fieldbackground=[('readonly',colors.background)])
        
        ttk_style.configure('TSpinbox', borderwidth=0,background=colors.background)
        ttk_style.map('TSpinbox', borderwidth=[('selected', 1)])
        
        # icon
        # ~ self.set_icon(root)
        
        # event bindings
        root.protocol("WM_DELETE_WINDOW",self.on_closing)
        
        # drawing styles
        self.style = {'linestyle':'None',
                      'linewidth':mpl.rcParams['lines.linewidth'],
                      'marker':'.',
                      'markersize':mpl.rcParams['lines.markersize'],
                      'capsize':0.,
                      'elinewidth':mpl.rcParams['lines.linewidth'],
                      'alpha':1.,
                      'fillstyle':'full'}
        
        # main frame
        self.mainframe = ttk.Frame(root,pad=5)
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        # Menu bar options ----------------------------------------------------
        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        root['menu'] = menubar
        
        # File
        menu_file = Menu(menubar)
        menu_file.add_command(label='Save State',command=self.save)
        menu_file.add_command(label='Load State',command=self.load)
        menu_file.add_command(label='Close All Figures',command=self.close_all)
        menu_file.add_command(label='Exit',command=sys.exit)
        menubar.add_cascade(menu=menu_file, label='File')
        
        
        # Top Notebook --------------------------------------------------------
        noteframe = ttk.Frame(self.mainframe,relief='sunken',pad=5)
        self.notebook = ttk.Notebook(noteframe)
        
        # Buttons -------------------------------------------------------------
        button_add_file = ttk.Button(self.mainframe, text='Add Image',
                                     command=self.add_file,pad=5)
        button_addlast_file = ttk.Button(self.mainframe, text='Add Last',
                                     command=self.addlast_file,pad=5)
        button_target = ttk.Button(self.mainframe, text='New Target',
                                     command=self.addtarget,pad=5)
        
        # gridding
        self.notebook.grid(column=0,row=0,sticky=(N,E,W,S))
        button_add_file.grid(column=0,row=1,sticky=(E,S))
        button_addlast_file.grid(column=1,row=1,sticky=(E,S))
        button_target.grid(column=2,row=1,sticky=(E,S))
        noteframe.grid(column=0,row=0,sticky=(N,E,W,S))
        noteframe.columnconfigure(0,weight=1)
        noteframe.rowconfigure(0,weight=1)

        # runloop
        self.root.mainloop()
    
    # ======================================================================= #
    def add_file(self):
        """
            Add tab based on new file
        """
        
        # get data
        
        # start file browser
        
        
        
        # ~ new_tab = ttk.Frame(notebook)
        # ~ self.notebook.add(file_viewer_tab,text='Filename')
        
        pass
        
    # ======================================================================= #
    def addlast_file(self):
        """
            Add tab based on last modified file
        """
        pass
        
    # ======================================================================= #
    def addtarget(self):
        """
            Add new target to drawn windows
        """
        pass
        
    # ======================================================================= #
    def close_all(self):
        """Close all open figures"""
        plt.close('all')
        # ~ for k in self.plt.plots:    self.plt.plots[k] = []
        # ~ for k in self.plt.active:   self.plt.active[k] = 0

    # ====================================================================== #
    def on_closing(self):
        """Excecute this when window is closed: destroy and close all plots."""
        # ~ self.logger.info('Closing all windows.')
        # ~ plt.close('all')
        self.root.destroy()
        # ~ self.logger.info('Finished     ' + '-'*50)
    
    # ====================================================================== #
    def load(self):
        """
            Load all internal variables from save file
        """
        pass
    
    # ====================================================================== #
    def save(self):
        """
            Save all internal variables for later loading
        """
        pass
