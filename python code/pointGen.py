#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 10:20:50 2017

@author: Franklin
"""
import numpy as np
import json
from math import *
import matplotlib.pyplot as plt


class pointGen():
    def __init__(self, max_step):
        #Generate the x,y coordinates for surface probe commands based on an circular craniotomy offset from bregma.
        self.writeProbeGCode(max_step)
        
    def writeProbeGCode(self, max_step):
        #all units are in mm
        
        # Polishing
        #left side polish y
        #logo_coordinates = [[-3.5,-3.5,-3.5,-3.5,-3.5,-3.35,-3.35,-3.35,-3.35,-3.35,-3.2,-3.2,-3.2,-3.2,-3.2,-3.05,-3.05,-3.05,-3.05,-3.05,-2.9,-2.9,-2.9,-2.9,-2.9,-2.75,-2.75,-2.75,-2.75,-2.75,-2.6,-2.6,-2.6,-2.6,-2.6,-2.45,-2.45,-2.45,-2.45,-2.45,-2.3,-2.3,-2.3,-2.3,-2.3,-2.15,-2.15,-2.15,-2.15,-2.15,-2,-2,-2,-2,-2,-1.85,-1.85,-1.85,-1.85,-1.85,-1.7,-1.7,-1.7,-1.7,-1.7],
        #                    [-3.5,-3,-2.5,-2,-1.5,-1.5,-2,-2.5,-3,-3.5,-3.5,-3,-2.5,-2,-1.5,-1.5,-2,-2.5,-3,-3.5,-3.5,-3,-2.5,-2,-1.5,-1.5,-2,-2.5,-3,-3.5,-3.5,-3,-2.5,-2,-1.5,-1.5,-2,-2.5,-3,-3.5,-3.5,-3,-2.5,-2,-1.5,-1.5,-2,-2.5,-3,-3.5,-3.5,-3,-2.5,-2,-1.5,-1.5,-2,-2.5,-3,-3.5,-3.5,-3,-2.5,-2,-1.5]]
        
        #left side polish x
        #logo_coordinates = [[-3.5,-3.35,-3.2,-3.05,-2.9,-2.75,-2.6,-2.45,-2.3,-2.15,-2,-1.85,-1.7,-3.5,-3.35,-3.2,-3.05,-2.9,-2.75,-2.6,-2.45,-2.3,-2.15,-2,-1.85,-1.7,-3.5,-3.35,-3.2,-3.05,-2.9,-2.75,-2.6,-2.45,-2.3,-2.15,-2,-1.85,-1.7,-3.5,-3.35,-3.2,-3.05,-2.9,-2.75,-2.6,-2.45,-2.3,-2.15,-2,-1.85,-1.7,-3.5,-3.35,-3.2,-3.05,-2.9,-2.75,-2.6,-2.45,-2.3,-2.15,-2,-1.85,-1.7],
         #                   [-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3.5,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2.5,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5]]
        
        
        #Craniotomy shapes
        
        #right rectangle example 
        #logo_coordinates = [[1.1,2.6,2.6,1.1,1.1],
        #                    [2.5,2.5,-4,-4,2.5]]

        #cerebellum
        #logo_coordinates = [[-4.5,-4,4,4.5],
        #                    [-7,-8,-8,-7]]
           
        
        #Check step size between points and compare to max_step
        num_steps = len(logo_coordinates[0])-1
        n=0
        for x in range(num_steps):
            #Caculate distance between two steps. Do we need to interpolate?
            #DEBUG print("n={}".format(n))
            a = logo_coordinates[0][n+1]-logo_coordinates[0][n]
            #DEBUG print("a={}".format(a))
            b = logo_coordinates[1][n+1]-logo_coordinates[1][n]
            #DEBUG print("b={}".format(b))
            L = sqrt(a*a+b*b)
            #DEBUG print("L={}".format(L))
            if L > max_step:
                num_interp = int(ceil(L/max_step))
                #DEBUG print(num_interp)
                x_inc = a/num_interp
                y_inc = b/num_interp
                for m in range(num_interp-1):
                    #DEBUG print("m={}".format(m))
                    x_start = logo_coordinates[0][n]
                    y_start = logo_coordinates[1][n]
                    logo_coordinates[0].insert(n+m+1, x_start + (m+1)*x_inc)
                    logo_coordinates[1].insert(n+m+1, y_start + (m+1)*y_inc)
                n = n+num_interp
                    
            else:
                #DEBUG print("step is OK")
                n=n+1
        
        
        
        logo_coordinates[0] = [round(x,4) for x in logo_coordinates[0]]
        logo_coordinates[1] = [round(x,4) for x in logo_coordinates[1]]
        '''
        logo_coordinates[0] = logo_coordinates[0][:-1]
        logo_coordinates[1] = logo_coordinates[1][:-1]
        '''
        plt.plot(logo_coordinates[0],logo_coordinates[1],'r.')
        plt.plot(logo_coordinates[0],logo_coordinates[1],'k-')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        
                
        self.gCode = list()
        
        #First, set the current position (bregma) as the origin
        gc_line = {"gc":"g28.3x0y0z0"}
        number_pts = len(logo_coordinates[0])
        self.gCode.append(gc_line)
        for num in range(0,number_pts):
            #Now, raise up z 0.5mm for clearance. Traverse to new (x,y) and run g38.2 probe command. Reapeat for each (x,y).
            gc_line = {"gc":"g91g1f100z0.5"}
            self.gCode.append(gc_line)
            
            gc_line = {"gc":"g90g1f100x{:.4f}y{:.4f}" .format(logo_coordinates[0][num],logo_coordinates[1][num])}
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

       
