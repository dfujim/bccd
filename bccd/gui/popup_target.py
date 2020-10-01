# Popup to set target settings
# Derek Fujimoto
# Sep 2020

from tkinter import *
from tkinter import ttk
import textwrap

from bccd.backend import colors

# ========================================================================== #
class popup_target(object):
    """
        Popup window for setting targeting options. 
        
        Data fields: 
            win: toplevel window
            frame_color: tk frame for showing the color of the target lines
            shape: StringVar, stores shape to draw
    """

    description = '\n'.join(textwrap.wrap("Draw a shape in the active figure, "+\
                                "synchronized across multiple figures.",width=30))
                    
    # colours in the default matplotlib cycle
    colors = {  'C0':'#1f77b4',
                'C1':'#ff7f0e', 
                'C2':'#2ca02c', 
                'C3':'#d62728',
                'C4':'#9467bd',
                'C5':'#8c564b', 
                'C6':'#e377c2',
                'C7':'#7f7f7f',
                'C8':'#bcbd22',
                'C9':'#17becf',
                }

    # ====================================================================== #
    def __init__(self, bccd):
        self.bccd = bccd
        
        # make a new window
        win = Toplevel(bccd.mainframe)
        win.title('Set and Draw Target')
        
        # icon
        # ~ parent.set_icon(self.win)
        
        # Key bindings
        # ~ self.win.bind('<Return>',self.set)             
        # ~ self.win.bind('<KP_Enter>',self.set)
    
        # Column0 ----------------------------------------------------------
        frame_col0 = ttk.Frame(win, relief='sunken', pad=5)
        frame_col0.grid(column=0, row=0, sticky=(N,S,E,W), padx=5, pady=5)
    
        # Colour swatch
        self.frame_color = Frame(frame_col0, width=200, height=30)
        self.frame_color.grid(column=0,row=0,sticky=(N,W,S,E), padx=10, pady=10)
        self.frame_color.columnconfigure(0,weight=1)
        self.frame_color.rowconfigure(0,weight=1)
        self.set_frame_color()
        
        # Header
        ttk.Label(frame_col0, text=self.description).grid(column=0, row=1,
                  sticky=(N,W), padx=10, pady=10)
        
        # Column1 ----------------------------------------------------------
        frame_col1 = ttk.Frame(win, relief='sunken', pad=5)
        frame_col1.grid(column=1, row=0, sticky=(N,S,E,W), padx=5, pady=5)
        
        self.shape = StringVar()
        R1 = ttk.Radiobutton(frame_col1, text="Circle", variable=self.shape, 
                            value='circle', selectcolor=colors.selected)
        R2 = ttk.Radiobutton(frame_col1, text="Square", variable=self.shape, 
                            value='square')
        R3 = ttk.Radiobutton(frame_col1, text="Ellipsis", variable=self.shape, 
                            value='ellipsis')
        R4 = ttk.Radiobutton(frame_col1, text="Rectangle", variable=self.shape, 
                            value='rectangle')
        
        R1.grid(column=0, row=0, sticky=(N,E,W))
        R2.grid(column=0, row=1, sticky=(N,E,W))
        R3.grid(column=0, row=2, sticky=(N,E,W))
        R4.grid(column=0, row=3, sticky=(N,E,W))
        
        self.win = win
        
    # ====================================================================== #
    def set_frame_color(self, color='#FFFFFF'):
        """
            Set the color frame color
        """
        
        if color in self.colors.keys():
            self.frame_color.config(bg=self.colors[color])
        else:
            self.frame_color.config(bg=color)
    
    # ====================================================================== #
    def cancel(self):
        self.win.destroy()

