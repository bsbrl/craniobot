#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:26:21 2017

@author: Franklin
"""

import numpy as np
import json
import plotly as py
import plotly.graph_objs as go


class MillPath():
    def __init__(self,probeOutput,depth):
        #Generate the x,y coordinates for surface probe commands based on an circular craniotomy offset from bregma.
        self.writeGCode(probeOutput,depth)
            
    def writeGCode(self, probeOutput, depth):
        #Now write the gcode probe routine to an output file
        self.gCode = list()
        self.millCoords = list([[],[],[],[]])
        
        #Raise the bit up from bregma
        new_line = {"gc":"g90g1f100z2"}
        self.gCode.append(new_line)
        
        #move over to the first (x,y) coordinate
        x = probeOutput[0]["r"]["prb"]["x"]
        y = probeOutput[0]["r"]["prb"]["y"]
        new_line = {"gc":"g90g1f100x{:.4f}y{:.4f}" .format(x,y)}
        self.gCode.append(new_line)
        
        #Drop down to the skull surface + the desired depth
        for item in probeOutput:
            x = item["r"]["prb"]["x"]
            y = item["r"]["prb"]["y"]
            z = item["r"]["prb"]["z"] - depth
            new_line = {"gc":"g90g1f10x{:.4f}y{:.4f}z{:.4f}".format(x,y,z)}
            self.gCode.append(new_line)
            self.millCoords[0].append(x)
            self.millCoords[1].append(y)
            self.millCoords[2].append(z)
            self.millCoords[3].append(item["r"]["prb"]["z"])
            
            
        
        #Final milling step is to return to the starting point of the contour
        x = probeOutput[0]["r"]["prb"]["x"]
        y = probeOutput[0]["r"]["prb"]["y"]
        z = probeOutput[0]["r"]["prb"]["z"] - depth
        new_line = {"gc":"g90g1f5x{:.4f}y{:.4f}z{:.4f}".format(x,y,z)}
        self.gCode.append(new_line)
        self.millCoords[0].append(x)
        self.millCoords[1].append(y)
        self.millCoords[2].append(z)
        self.millCoords[3].append(probeOutput[0]["r"]["prb"]["z"])
        
        #Now lift up to 2mm above the top of the skull
        new_line = {"gc":"g90g1f100z2"}
        self.gCode.append(new_line)
        
        #Flag end of program
        new_line = {"gc":"m2"}
        self.gCode.append(new_line)
        
        #Plot the milling path
        trace1 = go.Scatter3d(
            x=self.millCoords[0],
            y=self.millCoords[1],
            z=self.millCoords[2],
            mode='lines+markers',
            marker=dict(
                size=4,
                line=dict(
                    color='rgba(217, 217, 217, 0.14)',
                    width=0.5
                ),
                opacity=0.8
            )
        )
        trace2 = go.Scatter3d(
            x=self.millCoords[0],
            y=self.millCoords[1],
            z=self.millCoords[3],
            mode='lines+markers',
            marker=dict(
                size=4,
                line=dict(
                    color='rgba(300, 300, 300, 0.14)',
                    width=0.5
                ),
                opacity=0.8
            )
        )
        data = [trace1, trace2]
        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )


        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig, filename='mill_path.html')
        
        
        
        
        
    def writeGCodeToFile(fileName):
        with open(fileName,'w') as f:
            for item in self.gCode:
                f.write('{}\n' .format(json.dumps(item)))
        
            
