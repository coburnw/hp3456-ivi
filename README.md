## Agilent HP3456A Digital Voltmeter driver for Python-IVI

A simple but functional driver for interacting with the HP 3456A series voltmeters

### Requirements
  * developed using Python 2.7.9
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  * untested with the other python-ivi gpib interface drivers

### Installation
Since the installation is very similar for each of my IVI drivers, see this [gist] (https://gist.github.com/coburnw/57634c7e821dd7f32e9a68e1d14c16a4) 

### Notes
  * Developed for an HP3456A and an E2050A. Other devices and options untested.
  * None of the trigger, memory, or math functionality has been implemented.

Altho my meter seemed to work fine at the fleamarket, after getting it home i found that it had what appeared to be three unrelated problems.  Much time was spent with the end result of building an eprom adapter board http://tindie.com/products/10177/ with new memory.  I now have a wonderful, fully functioning meter.

This has been a fun trip and I greatly appreciate the work the Python-IVI
developers have invested.
