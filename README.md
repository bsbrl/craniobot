# craniobot

1. System requirements

a. Software dependencies
- Windows 10
- 64 bit
- Internet connection
b. This software has only been tested on windows 10 64 bit systems
c. Required non-standard hardware
- See manuscript for custom hardware description
- TinyG (~30-45 minutes)
	- Install hardware according to - https://github.com/synthetos/TinyG/wiki/TinyG-Start (you do not need a fan nor a program debugger)
	- Connect Tiny G according to - https://github.com/synthetos/TinyG/wiki/Connecting-TinyG
	- For custom notes on our installation see "Tiny G Seup.docx"

2. Installation

a. Download software (~10-15 minutes)
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

b. Upload arduino file (~3-10 minutes)
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

c. Change tinyG COM port in python code (~3-10 minutes)
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


3. Demo
a. Instructions to run on data
b. Expected output
c. Expected run time

4. Instructions for use
a. How to run software on your data
