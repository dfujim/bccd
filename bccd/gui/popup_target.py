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
                
    shapes = ('circle','square','ellipsis','rectangle')

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
        
        # draw shape radio buttons
        self.shape = StringVar()
        radios = []
        for i,v in enumerate(self.shapes):
            rad = ttk.Radiobutton(frame_col1, 
                            text=v.title().rjust(max([len(s) for s in self.shapes])), 
                            variable=self.shape, 
                            value=v)
            rad.grid(column=0, row=i, sticky=(N,W))
            radios.append(rad)
            frame_col1.rowconfigure(i,weight=1)
            
            
        self.shape.set(self.shapes[0])
        
        self.win = win
        
        # Row2 ----------------------------------------------------------
        
        frame_row2 = ttk.Frame(win, relief='sunken', pad=5)
        frame_row2.grid(column=0, row=1, sticky=(N,S,E,W), padx=5, pady=5, columnspan=2)
        frame_row2.columnconfigure(0,weight=1)
        frame_row2.columnconfigure(1,weight=1)
        
        # buttons
        button_draw = ttk.Button(frame_row2, text='Draw', command=self.draw)
        button_remove = ttk.Button(frame_row2, text='Remove', command=self.remove)
        
        button_draw.grid(column=1,   row=0, sticky=(N,E,W,S))
        button_remove.grid(column=0, row=0, sticky=(N,E,W,S))
        
        
    # ====================================================================== #
    def draw(self):
        """
            Add the target to the open figure
        """
        pass
    
    # ====================================================================== #
    def remove(self):
        """
            Remove the target from the open figure
        """
        pass
        
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

