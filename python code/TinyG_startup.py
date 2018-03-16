    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 12:52:40 2017

@author: Franklin
"""

from CNCController import CNCController as CNC
from generateCircularCraniotomy import GenerateCircularCraniotomy
from generate_milling_commands import MillPath
from pointGen import pointGen


tinyG = CNC()
tinyG.assignPort("default")
tinyG.connect()
tinyG.checkConnection()

"""
#Use this code to generate probe commands for a circular craniotomy

craniotomy = GenerateCircularCraniotomy(0,0,3,10)
probe_commands = craniotomy.gCode
"""



