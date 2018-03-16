#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:41:05 2017

@author: Franklin
"""

import serial
import time
import json
from pointGen import pointGen

class CNCController():   
    
    def assignPort(self,port):
        if port.lower() == 'default':
            self.port = 'COM4' #change this com port to the com port of your tinyG
            #self.port = '/dev/tty.usbserial-DN01XFHI'
        else:
            self.port = port
        
    def checkConnection(self):
        #This checks the connection state of the Serial port
        #If ser doesn't exist, print Open serial port.
        self.flag = False
        try:
            if self.ser.isOpen():
                print("CNC port is open at " + self.port)
            else:
                print(self.port + " is closed")
                self.flag = True
        except AttributeError:
            print("Need to first open the serial port connection!")
            self.flag = True
        #return flag
        
    
    def connect(self):
        #This opens up the serial port connection to the CNC machine.
        self.ser = serial.Serial(self.port, baudrate = 115200, timeout=1)
        

    def disconnect(self):
        #This closes the serial port connection to the CNC machine.
        self.ser.close()
        
    def jog(self, direction, step, speed):
        #This is used to jog the machine
        command = '{{"gc":"g91g1f{}{}{}"}}\n'.format(speed, direction, step)
        self.ser.write(command.encode('utf-8'))
    
    def goToXYOrigin(self, speed):
        #This will take the machine to (x,y)=(0,0) at any z
        command = '{{"gc":"g90g1f{}x0y0"}}\n'.format(speed)
        self.ser.write(command.encode('utf-8'))
    
    def runSingleProbe(self):
        command = {"gc":"g38.2f5z-5"} # probe down/up to -5mm at a rate of 5 mm/min
        self.ser.write('{}\n' .format(json.dumps(command)).encode('utf-8'))
    
    def setOrigin(self):
        #This sets the current position to (0,0,0)
        self.ser.write(b'{"gc":"g28.3x0y0z0"}\n')
        
    def currentPosition(self):
        #This returns the current position of the CNC machine
        self.ser.write(b'{"pos":n}\n')
        if self.ser.inWaiting:           #Is there anything to read?
            print(self.ser.readlines())
        
    def wakeUp(self):
        #This wakes up the CNC machine if it's been idle for awhile
        self.ser.write(b'\r\n\r\n\r\n')
        time.sleep(2)
        
                   #Is there anything to read?
        while self.ser.inWaiting():
            num_bytes = self.ser.inWaiting()
            message = self.ser.read(num_bytes).decode('ascii')
            print(message)
        
    def checkConfiguration(self):
        #This checks that the configuration of TinyG is set approriately for the code
        self.ser.write(b'{"sys":n}\n')
        print("Checking that the TinyG configuration settings are correct...\n")
        time.sleep(2)
        configuration = list()
        flag = False
        while self.ser.inWaiting():
            configuration.append(json.loads(self.ser.readline().decode('ascii'))) #Get the response and parse as JSON
            if configuration[-1]["r"]["sys"]["jv"] != 5:
                print("JSON reporting verbosity is configured incorrectly\n")
                flag = True
            else:
                print("JSON verbosity set correctly to 5! Safe to continue.\n")
            if configuration[-1]["r"]["sys"]["qv"]:
                print("The queue report verbosity settings are incorrectly set to 1.\n")
                flag = True
            else:
                print("The queue report verbosity settings are correct! Safe to continue.\n")
            if configuration[-1]["r"]["sys"]["sv"]:
                print("The status report verbosity settings are incorrectly set to 1.\n")
                flag = True
            else:
                print("The status report verbosity settings are correct! Safe to continue.\n")
        return flag
        

        
    def runProbe(self,gCode):
      
        reports = list() # An empty list to store status reports from TinyG
        
        
        if self.checkConnection():  #Make sure we have a connection
            print("Connection issue. Please try again.")
            return
        
        self.ser.flushInput()            #Flush startup text in serial input
        self.wakeUp()
        if self.checkConfiguration():  #make sure configuration settings are correct and OK to continue
            print("The configuration is set incorrectly. Please fix")
            return
        
        #Send a few lines of gcode to get the TinyG planning buffer filled a bit
        n=5
        for x in range(n):
            #self.ser.write(probe_commands[x].encode('utf-8'))
            self.ser.write('{}\n'.format(json.dumps(gCode[x])).encode('utf-8'))
        
        #Now send a new line of gcode every time TinyG returns a status saying it's completed a line of gcode
        #This prevents over filling the planning buffer. Do this until we've made it through the entire code.
        #See https://github.com/synthetos/TinyG/issues/175 for more info 
        #and also https://onehossshay.wordpress.com/2011/08/26/grbl-a-simple-python-interface/
        
        while n<len(gCode):
            if self.ser.inWaiting(): #is there something to be read?
                reports.append(json.loads(self.ser.readline().decode('ascii'))) #Get the response and parse as JSON
                if "gc" in reports[-1]["r"]: #if we get a system report saying a gCode command is complete, send another line of gcode.    
                    #self.ser.write(probe_commands[n].encode('utf-8'))
                    self.ser.write('{}\n'.format(json.dumps(gCode[n])).encode('utf-8'))
                    runProbe_percent_complete = n/len(gCode)*100 #matt
                    print("runProbe progress: ", runProbe_percent_complete, "%") #matt
                    n+=1   #index the while loop and loop back until we've sent all the gcode commands.

                    
             
        while "m2" not in json.dumps(reports[-1]).lower():  #now sit and read the serial line until the program end flag is sent by TinyG
            if self.ser.inWaiting():
                reports.append(json.loads(self.ser.readline().decode('ascii')))  #read out remaining serial output from Tiny g until last entry is an empty string
                
        
        self.probe_output = [item for item in reports if "prb" in item["r"]] #filter out only probe end returns, and convert the strings to JSON.
        #return probe_output


    def runMill(self,gCode):
        reports = list() # An empty list to store status reports from TinyG
        if self.checkConnection():  #Make sure we have a connection
            print("Connection issue. Please try again.")
            return
        
        
        self.ser.flushInput()            #Flush startup text in serial input
        self.wakeUp()
        if self.checkConfiguration():  #make sure configuration settings are correct and OK to continue
            print("The configuration is set incorrectly. Please fix")
            return
        
        #Send a few lines of gcode to get the TinyG planning buffer filled a bit
        n=5
        for x in range(n):
            '''#self.ser.write(probe_commands[x].encode('utf-8'))'''
            self.ser.write('{}\n'.format(json.dumps(gCode[x])).encode('utf-8'))
        
        #Now send a new line of gcode every time TinyG returns a status saying it's completed a line of gcode
        #This prevents over filling the planning buffer. Do this until we've made it through the entire code.
        #See https://github.com/synthetos/TinyG/issues/175 for more info 
        #and also https://onehossshay.wordpress.com/2011/08/26/grbl-a-simple-python-interface/
        
        while n<len(gCode):
            if self.ser.inWaiting(): #is there something to be read?
                reports.append(json.loads(self.ser.readline().decode('ascii'))) #Get the response and parse as JSON
                if "gc" in reports[-1]["r"]: #if we get a system report saying a gCode command is complete, send another line of gcode.    
                    #self.ser.write(probe_commands[n].encode('utf-8'))
                    self.ser.write('{}\n'.format(json.dumps(gCode[n])).encode('utf-8'))
                    n+=1   #index the while loop and loop back until we've sent all the gcode commands.
                   
                    
             
        while "m2" not in json.dumps(reports[-1]).lower():  #now sit and read the serial line until the program end flag is sent by TinyG
            if self.ser.inWaiting():
                reports.append(json.loads(self.ser.readline().decode('ascii')))  #read out remaining serial output from Tiny g until last entry is an empty string.
        
        return reports
        
    
