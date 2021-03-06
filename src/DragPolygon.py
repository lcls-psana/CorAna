#!/usr/bin/env python
#----------------------------------
from __future__ import print_function
from __future__ import absolute_import
import sys

import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.lines  as lines
import math # cos(x), sin(x), radians(x), degrees()
from .Drag import *

class DragPolygon( Drag, lines.Line2D ) :

    def __init__(self, x=None, y=None, linewidth=2, color='b', picker=5, linestyle='-', str_of_pars=None) :

        Drag.__init__(self, linewidth, color, linestyle, my_type='Polygon')

        if str_of_pars is not None : # Initialization for input from file
            t,lw,col,s,r,nvtx,self.xarr,self.yarr = self.parse_str_of_pars(str_of_pars)
            self.isSelected    = s
            self.myType        = t
            self.isRemoved     = r
            self.isInitialized = True
            lines.Line2D.__init__(self, self.xarr, self.yarr, linewidth=lw, color=col, picker=picker)
            #self.print_pars()

        elif x is None or y is None : # Default line initialization
            lines.Line2D.__init__(self, (0,1), (0,1), linewidth=linewidth, color=color, picker=picker)
            self.isInitialized = False
        else :
            lines.Line2D.__init__(self,  x,  y, linewidth=linewidth, color=color, picker=picker)
            self.isInitialized = True

        self.set_pickradius(picker)
        self.press    = None
        self.myPicker = picker
        self.vtx      = 0


    #def set_dragged_obj_properties(self):
    #    self.set_color    ('k')
    #    self.set_linewidth(1)
    #    self.set_linestyle('--') #'--', ':'

    def get_list_of_pars(self) :
        xarr, yarr = self.get_data()
        nvtx1      = len(xarr)
        lw  = int( self.get_linewidth() ) 
        col = self.myCurrentColor
        s   = self.isSelected
        t   = self.myType
        r   = self.isRemoved
        return (t,lw,col,s,r,nvtx1,xarr,yarr)


    def parse_str_of_pars(self, str_of_pars) :
        pars = str_of_pars.split()
        #print 'parse_str_of_pars:', pars
        t    = pars[0]
        lw   = int(pars[1])
        col  = str(pars[2])
        s    = self.dicBool[pars[3].lower()]
        r    = self.dicBool[pars[4].lower()]
        nvtx1= int(pars[5])
        xarr = [float(pars[i+6])       for i in range(nvtx1)]
        yarr = [float(pars[i+6+nvtx1]) for i in range(nvtx1)]
        return (t,lw,col,s,r,nvtx1,xarr,yarr)


    def get_str_of_pars(self) :
        t,lw,col,s,r,nvtx1,xarr,yarr = self.get_list_of_pars()
        str_of_pars = '%s %d %s %s %s %d ' % (t,lw,col,s,r,nvtx1)
        str_of_xarr = ''
        str_of_yarr = ''
        for x in xarr : str_of_xarr+='%7.2d ' % (x)
        for y in yarr : str_of_yarr+='%7.2d ' % (y)
        return str_of_pars + str_of_xarr + str_of_yarr


    def print_pars(self) :
        print('t,lw,col,s,r,nvtx1,xarr,yarr =', self.get_str_of_pars())


    def on_press(self, event):
        """on button press we will see if the mouse is over us and store some data"""
        if event.inaxes != self.axes: return

        clickxy = (event.xdata, event.ydata)
        #print 'clickxy =',clickxy

        if self.isInitialized :
            contains, attrd = self.contains(event)
            #contains = self.contains(event)
            if not contains: return

            xarr, yarr = self.get_data()

            self.dx_prev, self.dy_prev = 0, 0

            # find vertex closest to the click
            self.dist_min=10000
            for ind, xy in enumerate(zip(xarr,yarr)) :
                dist = self.max_deviation(clickxy, xy)
                if dist < self.dist_min :
                    self.dist_min = dist
                    self.vtx = ind

            self.press = clickxy, (xarr[self.vtx], yarr[self.vtx])

            #----Remove object at click on middle mouse botton
            if event.button is 2 : # for middle mouse button
                self.remove_object_from_img() # Remove object from image
                return

        else : # if the line position is not defined yet, when it is added:

            if event.button is 2 : # Ignore middle button at initialization
                return

            if self.vtx == 0 :
                self.xarr = [clickxy[0]]
                self.yarr = [clickxy[1]]

            
            # Try to prevent double-clicks
            if self.vtx>1 and clickxy == (self.xarr[self.vtx-1], self.yarr[self.vtx-1]) : return

            self.vtx += 1
            self.xarr.append(clickxy[0]+1) # take it twise, will be changed...
            self.yarr.append(clickxy[1]+1)

            self.press = clickxy, clickxy

        self.on_press_graphic_manipulations()


    def on_motion(self, event):
        """on motion we will move the rect if the mouse is over us"""
        if event.inaxes != self.axes: return

        if self.press is None: return

        #print 'event on_moution', self.get_xydata()
        currentxy = event.xdata, event.ydata

        (x0, y0), (xv, yv) = self.press

        # Move/edit polyline
        if self.isInitialized : 
            dx = currentxy[0] - x0
            dy = currentxy[1] - y0

            # Move a single vertex
            if event.button is 1 : # for left mouse button
                self.xarr[self.vtx] = xv + dx
                self.yarr[self.vtx] = yv + dy

                # Keep polygon closed in motion of 0 and last vertex
                if self.vtx == 0 :
                    self.xarr[-1] = self.xarr[0]
                    self.yarr[-1] = self.yarr[0]
                    
                if self.vtx == len(self.xarr)-1 :
                    self.xarr[0] = self.xarr[-1]
                    self.yarr[0] = self.yarr[-1]

            # Move entire polylane
            if event.button is 3 : # for right mouse button
                for vi in range(len(self.xarr)) :
                    self.xarr[vi] += dx - self.dx_prev
                    self.yarr[vi] += dy - self.dy_prev

                self.dx_prev, self.dy_prev = dx, dy
            
        # Draw continuation of the poly-line to the next (moving) point
        else : # not initialized 
            self.xarr[self.vtx] = currentxy[0]
            self.yarr[self.vtx] = currentxy[1]
            #print 'self.xarr:',self.xarr

        #self.set_xdata(self.xarr)
        #self.set_ydata(self.yarr)
        self.set_data(self.xarr, self.yarr)

        self.on_motion_graphic_manipulations()


    def on_release(self, event):

        if self.isInitialized  :
            self.on_release_graphic_manipulations()
            #if self.press is not None : self.print_pars()
            if self.press is not None : self.maskIsAvailable = False        
            self.press = None

        else : # if not self.isInitialized
            if event.button is 2 : # Ignore middle button at initialization
                return

            if event.button is 3 :
                """on release we reset the press data"""

                self.xarr[self.vtx] = self.xarr[0]
                self.yarr[self.vtx] = self.yarr[0]
                self.set_data(self.xarr,self.yarr)
    
                self.on_release_graphic_manipulations()
                #if self.press is not None : self.print_pars()
                if self.press is not None : self.maskIsAvailable = False        
                self.press = None

#-----------------------------

    def get_poly_verts(self):
        """Creates a set of (closed) poly vertices for mask"""
        xarr, yarr = self.get_data()
        return list(zip(xarr, yarr))

#-----------------------------
#-----------------------------
#-----------------------------
# Test
#-----------------------------
#-----------------------------
#-----------------------------

from .DragObjectSet import *

#-----------------------------
#-----------------------------
 
def generate_list_of_objects(img_extent) :
    """Produce the list of initial random objects for test purpose.
    """
    xmin,xmax,ymin,ymax = img_extent 
    print('xmin,xmax,ymin,ymax = ', xmin,xmax,ymin,ymax)

    nobj = 10
    x = (xmin,xmax)
    y = ymin+(ymax-ymin)*np.random.rand(nobj,2)

    obj_list = []
    for ind in range(nobj) :
        obj = DragPolygon(x, y[ind], linewidth=2, color='g', picker=5, linestyle='-')
        obj_list.append(obj)

    return obj_list

#-----------------------------

def main_full_test():
    """Full test of the class DragRectangle, using the class DragObjectSet
       1. make a 2D plot
       2. make a list of random objects and add them to the plot
       3. use the class DragObjectSet to switch between Add/Move/Remove modes for full test of the DragPolygon
    """
    fig, axes, imsh = generate_test_image()
    list_of_objs = generate_list_of_objects(imsh.get_extent())

    t = DragObjectSet(fig, axes, DragPolygon, useKeyboard=True)
    t.set_list_of_objs(list_of_objs)

    plt.get_current_fig_manager().window.geometry('+50+10') # move(50, 10)
    plt.show()

#-----------------------------

def main_simple_test():
    """Simple test of the class DragRectangle.
       1. make a 2-d plot
       2. make a list of random objects and add them to the plot
       3. add one more object with initialization at 1st click-and-drag of mouse-left button
    """
    fig, axes, imsh = generate_test_image()
    list_of_objs = generate_list_of_objects(imsh.get_extent())

    #Add one more object
    obj = DragPolygon() # call W/O parameters => object will be initialized at first mouse click
    add_obj_to_axes(obj, axes, list_of_objs)

    #plt.get_current_fig_manager().window.move(50, 10)
    plt.get_current_fig_manager().window.geometry('+50+10')
    plt.show()

#-----------------------------

if __name__ == "__main__" :

    #main_simple_test()
    main_full_test()
    sys.exit ('End of test')

#-----------------------------


