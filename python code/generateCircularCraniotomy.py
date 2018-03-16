#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:03:28 2017

@author: Franklin
"""
import numpy as np
import json
import matplotlib.pyplot as plt

class GenerateCircularCraniotomy():
    def __init__(self,x_center,y_center,diameter,number_pts):
        #Generate the x,y coordinates for surface probe commands based on an circular craniotomy offset from bregma.
        self.number_pts = number_pts
        self.coordinates = np.zeros((number_pts,2))
        self.probe_commands = list()
        for n in range(0,number_pts):
            self.coordinates[n,0] = x_center + (diameter/2)*np.cos(n*np.radians(360)/number_pts)
            self.coordinates[n,1] = y_center + (diameter/2)*np.sin(n*np.radians(360)/number_pts)
        plt.axis([-8,8,-8,8])
        plt.plot(self.coordinates[:,0],self.coordinates[:,1])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        self.writeGCode()
            
    def writeGCode(self):
        #Now write the gcode probe routine to an output file
        self.gCode = list()
        
        #First, set the current position (bregma) as the origin
        gc_line = {"gc":"g28.3x0y0z0"}
        self.gCode.append(gc_line)
        for n in range(0,self.number_pts):
            #Now, raise up z 0.5mm for clearance. Traverse to new (x,y) and run g38.2 probe command. Reapeat for each (x,y).
            gc_line = {"gc":"g91g1f100z0.5"}
            self.gCode.append(gc_line)
            
            gc_line = {"gc":"g90g1f100x{:.4f}y{:.4f}" .format(self.coordinates[n,0],self.coordinates[n,1])}
            self.gCode.append(gc_line)
            
            gc_line = {"gc":"g38.2f5z-10"}
            self.gCode.append(gc_line)
        #End by going back to 1mm 
        gc_line = {"gc":"g90g1f100z1"}
        self.gCode.append(gc_line)
        
        gc_line = {"gc":"g90g1f100x0y0"}
        self.gCode.append(gc_line)
        
        #Now add a end of program m2 flag
        gc_line = {"gc":"m2"}
        self.gCode.append(gc_line)
        
