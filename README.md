# craniobot

# System requirements

1. Software dependencies
	- Windows 10
	- 64 bit
	- Internet connection
2. This software has only been tested on windows 10 64 bit systems
3.  Required non-standard hardware
	- See manuscript for custom hardware description
	- TinyG (~30-45 minutes)
		- Install hardware according to - https://github.com/synthetos/TinyG/wiki/TinyG-Start (you do not need a fan nor a program debugger)
		- Connect Tiny G according to - https://github.com/synthetos/TinyG/wiki/Connecting-TinyG
		- For custom notes on our installation see "Tiny G Seup.docx"

# Installation

1. Download software (~10-15 minutes)
	1. Download zip folder from ".zip" or download repository from https://github.com/bsbrl/craniobot
	2. Extract zipped folder
	3. Open notepad or any text editor
	4. Go to the folder "install", right open the file "install.bat" using notepad. If you do not see the file, select "All filetypes" from the dropdown in the windows explorer search, it defaults to only look for .txt files.
	5. Change the 'YOURPATHHERE' to the address of the folder that contains "intall.bat". For example if my folder with the file is C:/downloads/craniobot/install I would replace 'YOURPATHHERE' with 'C:/downloads/craniobot/install'.
	6. Save the file.
	7. Repeat steps 4-6 for the file titled "install2.bat"
	8. Right click the file "intall.bat" and click run as administrator. This will run the installation commands to install the following:
	- python 2.7.14
	- arduino-1.8.1-windows
	9. Add python to your path variable in windows as described in this tutorial
	https://www.pythoncentral.io/add-python-to-path-python-is-not-recognized-as-an-internal-or-external-command/
	10. Right click the file "install2.bat" and click run as administrator. This will download the following python packages.
	- python packages
		- numpy-1.14.2
		- matplotlib-2.2.0
		- plotly-2.5.0
		- pyserial-2.7

2. Upload arduino file (~3-10 minutes)
See https://www.arduino.cc/en/Guide/ArduinoDue to familiarize youself with the arduino editor and the arduino due and for trouble shooting help. 
	1. Connect the Arduino Due to the computer using a USB
	2. Double click the file "Surface_Probe.ino" located in the craniobot download folder. This will open the arduino editor.
	3. In the arduino editor click Tools>>BOARD>>Board Manager
	4. Search "due" in the search bar
	5. Install the Arduino SAM Boards file
	6. In the arduino editor click Tools>>BOARD>>Arduino Due (Programming Port)
	7. In the arduino editor click Tools>>PORT>>COM1. Note: The COM port may be COM1, COM2, COM3, COM4, COM5,... depending on the number of USB ports using serial communication on your computer. To figure out which port is the arduino, take note of all COM ports and then unplug the arduino USB. The port that is the arduino will no longer show up.
	8. Click the check mark beneath the file button. This will verify the code.
	9. Click the arrow next to the check mark, this will upload the file to the arduino.

3. Change tinyG COM port in python code (~3-10 minutes)
	1. To identify the COM port of your tinyG, go to the arduino application. You can search for arduino in your computer to find the application.
		- plug in your tinyG USB connetion and make sure your tinyG is turned on.
		- In the arduino editor click Tools>>PORT and look at the COM options (i.e. COM1, COM4, COM5 is shown)
		- Unplug the tinyG USB from your computer
		- In the arduino editor click Tools>>PORT>> and look at the COM options.
		- The COM of your tinyG port will no longer be on the list (i.e. COM1, COM4 is shown, this would mean COM5 is the tinyG port in this example).
	2. Plug the tinyG USB back into the computer
	3. Go to the file in the folder python titled "CNCController.py".
	4. Right click the file and click edit with IDLE
	5. Change the COM4 in "self.port = 'COM4' " to the serial port of your tiny G controller (i.e. in our example COM5 is the tinyG port so we would write self.port = 'COM5')
	6. Save the file and close the editor. 


# Demo
1. Instructions to run on data
To run all of the commands we will use the command line. Prepare the mouse
	1.	To run all of the commands we will use the command line. Search for command prompt in the windows search bar, and right click run as administrator. 
	2.	Locate the path to the craniobot folder called python code. I may look something like C:\downloads\craniobot\python code
	3.	In the command prompt type
```
Cd C:\downloads\craniobot\python code
```

	7.	Ensure the tinyG is not in an error/sleep state. Since this is the start of the procedure, reinitialize everything via switching power off and then on. 
	8.	Run tinyG_startup.py, it should connect to COM port 4
	9.	In the case that it was not reinitialized, tinyG.wakeUp() will wake it up, or a jog command input twice will wake it up, then jog in the desired step/rate.
	10.	Jog the end mill up (and away in xy directions if needed) to situate the mouse in the stereotax: tinyG.jog(“z”,1,200) input multiple times can accomplish this.
	11.	Remove the skin, fat, and fascia covering the dorsal skull.
	12.	Move the probe away from the mouse using jog commands, usually 15mm right and 15mm down tinyG.jog(“x”,15,200), then tinyG.jog(“y”,-15,200) and put the probe onto the mouse.
	13.	Move the probe above bregma using jog commands.
	14.	tinyG.runSingleProbe(), probe moves down to bregma and stops when contact sensor switch opens
	15.	tinyG.setOrigin()
	16.	for non-cicular craniotomies, make sure logo_coordinates contains two vectors for x and y coordinates in mm. Use BrainWindow(step_size) to generate pilot points. Ex: bw = BrainWindow(0.3) would be logo_coordinates with the minimum step size between points being 0.3 mm; extra points would be added to ensure this.
	17.	tinyG.currentPosition() to check if origin registered correctly, and at origin
	18.	tinyG.runProbe(bw.gCode) to begin probing at each point. 
	19.	Store tinyG.probe_output data into external container, ex: bw_out = tinyG.probe_output
	20.	Move probe away from skull, switch end mill to cutting tool, move the tool back to bregma (very precisely), all using jog commands
	21.	tinyG.setOrigin()
	22.	Generate mill path: path = MillPath(tinyG.probe_output, depth). If you are doing a skull thinning procedure, comment out lines that return the milling path to the initial point before generating the mill path in generate_milling_commands (lines 49 to 58). Usually I name my milling path by putting the depth into the variable, e.g. w50 = MillPath(bw_out, 0.050) would be for milling 50 um deep. Generate as many milling paths as you anticipate needing (you can generate them in later/earlier steps).
	23.	Examine the mill path to make sure there aren’t false positives.
	24.	tinyG.currentPotision()
	25.	tinyG.runMill(path.gCode), or going along with previous examples, tinyG.runMill(w50.gCode)
	26.	repeat for as many iterations/paths as needed.
	27.	Finished with craniobot part of surgery

2. Expected output
3. Expected run time

# Instructions for use
1. How to run software on your data
