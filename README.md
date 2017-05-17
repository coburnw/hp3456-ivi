## Agilent HP3456A Digital Voltmeter driver for Python-IVI

A simple but functional driver for interacting with the HP 3456A series voltmeters

### Requirements
  * developed using Python 2.7.9
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  * untested with the other python-ivi gpib interface drivers
  
### Installation
  Three installation methods
  
#### I know what I'm doing
  * Copy the new driver files into the Python-IVI tree
  * Adjust `__init__.py` files accordingly
  * rebuild and reinstall python-ivi
  * watch the digits roll
  
#### I want to know what I'm doing
  Inside the python-ivi source tree I made a contrib folder to store
  additional drivers. This was to minimize the amount of tromping around i would
  have to do in someone else's tree.  The `__init__.py` files need to be adjusted up
  the tree to account for the changes in structure including `config.py` at the root
  only once, while the `__init__.py` file in contrib needs to accurately reflect
  any changes to the contents of the contrib folder.

  An easier way to handle this might be to copy the new drivers directly into
  python-ivi/ivi/agilent folder and adjusting its `__init__.py` file accordingly.
  This might be a safer bet if you git pull python-ivi now and then.

  Regardless of the installation method chosen, the python-ivi package must
  be rebuilt and reinstalled each time a file inside its tree is added or modified.
  If you develop your application outside of the python-ivi tree, then a
  rebuild should hopefully be a rare occasion.

#### Spell it out for me (I'll try as best as i recall)
  * git clone https://github.com/coburnw/hp3456-ivi.git to a directory of your
    choice.  For me it was the parent folder containing the python-ivi clone folder.
  * if it doesnt already exist, mkdir python-ivi/ivi/contrib
  * cp hp3456-ivi.git/contrib/agilent*.py to python-ivi/ivi/contrib folder
  * edit `python-ivi/ivi/contrib/__init__.py` file to add the agilent3456A driver 
  * edit `python-ivi/ivi/__init__.py` and add 'contrib' to IVI drivers section
  * edit `python-ivi/setup.py` and verify 'contrib' is listed in the IVI drivers section
  * `python setup.py install` to (re)build and (re)install python-ivi
  * explore the example folder

### Notes
  * developed for an HP3456A and an E2050A. Other devices and options untested.
  * if any of the driver files are modified, python-ivi will need to be rebuilt
  and reinstalled
  * None of the trigger, memory, or math functionality has been implemented

This has been a fun trip and I greatly appreciate the work the Python-IVI
developers have invested.
