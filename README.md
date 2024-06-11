## HP3456A Digital Voltmeter driver for Python-IVI

A simple but functional driver for interacting with the HP 3456A series Voltmeters

### Requirements
  * developed using Python 2.7.9
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11

### Installation
Using pip to install in editable mode seems the cleanest way to avoid pythons import troubles.
Editable allows one to make changes to the repository and have them instantly available in
their applicaton. As an aside, using ```pip install -e .``` works perfectly well for both
python-ivi and the python-vxi11 repositories as well.
  * cd into repository
  * ```pip install -e .```
  
If pip refuses to install with an 'editable mode' error,
see [here](https://stackoverflow.com/a/73779542) for upgrading pip.

### Notes
  * Developed for an HP3456A and an E2050A. Other devices and options untested.
  * None of the trigger, memory, or math functionality has been implemented.
  * with my older instruments, i had to define instr.term_char = '\n'.  I found
    this caused a conversion error during pack_int() of the python-vxi11
    library.  If you have the same problem, notes on how i worked around it are
    [here](https://github.com/python-ivi/python-vxi11/pull/26/commits/d6205bf8dd298a5b629304e5853595510519432c)

Altho my meter seemed to work fine at the fleamarket, after getting it home i found
that it had what appeared to be three unrelated problems.  Much time was spent with
the end result of building an eprom adapter board http://tindie.com/products/10177/
with modern memory.  I now have a wonderful, fully functioning meter.

This has been a fun trip and I greatly appreciate the work the Python-IVI
developers have invested.
