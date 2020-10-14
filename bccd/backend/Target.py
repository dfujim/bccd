# Target for targeting
# Derek Fujimoto
# Sep 2020 

import matplotlib.patches as patches
from functools import partial

class Target(object):
    
    """
        Drawing shapes on lots of figures
        
        Data fields:
            ax_list: list of axis
            bccd: bccd object
            color: string, maplotlib color name for coloring everything
            draw_lines: function handle for drawing the target lines
            figures: list of figures to update
            patch: mpl.patches object to update
            label: ttk label object to update text on properties
            
    """

    # ======================================================================= #
    def __init__(self, popup_target, color, label):
        
        self.draw_lines = None
        self.figures = []
        self.bccd = popup_target.bccd 
        self.popup_target = popup_target 
        self.ax_list = []
        self.color = color
        self.label = label
        
        self.ax_list.append(self.bccd.plt.gca())

class Circle(Target):
    """
        Drawing circle target shapes on lots of figures
        
        Data fields:

    """

    # ======================================================================= #
    def __init__(self, popup_target, color, label, x, y, r):
        
        super().__init__(popup_target, color, label)
        
        # save circle position
        self.x = x
        self.y = y
        self.r = r
        
        # place circle at the center of the window
        self.circles = []
        
        # center
        self.pt_center = DraggablePoint(self,self.update_center,
                            setx=True,sety=True,color=self.color, marker='x')
        
        # radius
        self.pt_radius = DraggablePoint(self,self.update_radius,
                            setx=True,sety=False,color=self.color, marker='o')
        
        self.update_popup_label()
        
    # ======================================================================= #
    def draw(self, ax):
        """Add the target to the current axes"""
        
        self.circles.append(patches.Circle((self.x,self.y),self.r,
                                     fill=False, 
                                     facecolor='none',
                                     lw=1,
                                     ls='-',
                                     edgecolor=self.color))
        ax.add_patch(self.circles[-1])
        self.pt_center.add_ax(ax, self.x, self.y)
        self.pt_radius.add_ax(ax, self.x+self.r, self.y,)

    # ======================================================================= #
    def update_popup_label(self):
        """Update popup window label with info on target"""
        
        self.label.config(text='x = %d\ny = %d\nr = %d' % (self.x, self.y, self.r))
        
    # ======================================================================= #
    def update_center(self, x, y):
        """
            Update circle position based on DraggablePoint
        """
        self.pt_radius.set_xdata(x+self.r)
        self.pt_radius.set_ydata(y)
        
        for c in self.circles:
            c.set_center((x,y))
        
        self.x = x
        self.y = y
        self.update_popup_label()
    
    # ======================================================================= #
    def update_radius(self, x, y):
        """
            Update circle radius based on DraggablePoint
        """

        self.r = abs(self.x-x)
        
        for c in self.circles:
            c.set_radius(self.r)
            
        self.update_popup_label()
    
class Square(Target):
    """
        Drawing circle target shapes on lots of figures
        
        Data fields:

    """

    # ======================================================================= #
    def __init__(self):
        
        self.super().__init__()
        
class Rectangle(Target):
    """
        Drawing circle target shapes on lots of figures
        
        Data fields:

    """

    # ======================================================================= #
    def __init__(self):
        
        self.super().__init__()
        
class Ellipis(Target):
    """
        Drawing circle target shapes on lots of figures
        
        Data fields:

    """

    # ======================================================================= #
    def __init__(self):
        
        self.super().__init__()
        
class DraggablePoint:

    # http://stackoverflow.com/questions/21654008/matplotlib-drag-overlapping-points-interactively
    # https://stackoverflow.com/questions/28001655/draggable-line-with-draggable-points
    
    lock = None #  only one can be animated at a time
    size=0.01

    # ======================================================================= #
    def __init__(self,parent,updatefn,setx=True,sety=True,color=None, marker='s'):
        """
            parent: parent object
            points: list of point objects, corresponding to the various axes 
                    the target is drawn in 
            updatefn: funtion which updates the line in the correct way
                updatefn(xdata,ydata)
            x,y: initial point position
            setx,sety: if true, allow setting this parameter
            color: point color
        """
        self.parent = parent
        self.points = []
        self.color = color
        self.marker = marker
            
        self.updatefn = updatefn
        self.setx = setx
        self.sety = sety
        self.press = None
        self.background = None
        
    # ======================================================================= #
    def add_ax(self, ax, x=None, y=None):
        """Add axis to list of axes"""
        
        self.disconnect()
        
        
        if x is None:
            x = self.get_xdata()
        if y is None:
            y = self.get_ydata()
        self.points.append(ax.plot(x, y, zorder=100, color=self.color, alpha=0.5, 
                        marker=self.marker, markersize=8)[0])
        self.points[-1].set_pickradius(8)
        
        self.connect()
        
    # ======================================================================= #
    def connect(self):
        """connect to all the events we need"""
        
        self.cidpress = []
        self.cidrelease = []
        self.cidmotion = []
        
        for i,pt in enumerate(self.points):
            self.cidpress.append(pt.figure.canvas.mpl_connect('button_press_event', 
                                partial(self.on_press, id=i)))
                                 
            self.cidrelease.append(pt.figure.canvas.mpl_connect('button_release_event', 
                                self.on_release))
            self.cidmotion.append(pt.figure.canvas.mpl_connect('motion_notify_event', 
                                partial(self.on_motion, id=i)))

    # ======================================================================= #
    def on_press(self, event, id):
        
        if event.inaxes != self.points[id].axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.points[id].contains(event)
        if not contains: return
        DraggablePoint.lock = self
        
    # ======================================================================= #
    def on_motion(self, event, id):

        if DraggablePoint.lock is not self: return
        if event.inaxes != self.points[id].axes: return
        
        # get data
        x = event.xdata
        y = event.ydata
        
        # move the point
        if self.setx:   self.set_xdata(x)
        if self.sety:   self.set_ydata(y)

        # update the line
        self.updatefn(x,y)        

    # ======================================================================= #
    def on_release(self, event):
        'on release we reset the press data'
        if DraggablePoint.lock is not self: return
        DraggablePoint.lock = None
        
    # ======================================================================= #
    def disconnect(self):
        'disconnect all the stored connection ids'
        
        for i,pt in enumerate(self.points):
            pt.figure.canvas.mpl_disconnect(self.cidpress[i])
            pt.figure.canvas.mpl_disconnect(self.cidrelease[i])
            pt.figure.canvas.mpl_disconnect(self.cidmotion[i])

    # ======================================================================= #
    def get_xdata(self):
        """Get x coordinate"""
        return self.points[0].xdata
            
    # ======================================================================= #
    def get_ydata(self):
        """Get y coordinate"""
        return self.points[0].ydata
            
    # ======================================================================= #
    def set_xdata(self, x):
        """Set x coordinate"""
        for pt in self.points:
            pt.set_xdata(x)    
            
    # ======================================================================= #
    def set_ydata(self, y):
        """Set y coordinate"""
        for pt in self.points:
            pt.set_ydata(y)
