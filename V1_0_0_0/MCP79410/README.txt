
**********************************************************************************
MCP79410 Library:

MCP79410 is a python library used to interact with MCP79410 Real time Clock Calendar.
They were defined a lot of functions to interact with MCP79410 hardware. More functions
are usefull to interact with RTCC as TimeKeeper, alrms or TimeStamp. Other functions
are usefull to interact with internal EEPROM or with the protected EEPROM.

**********************************************************************************


**********************************************************************************
Requirements:

To use this library is necessary to have a "RTCC MCP79410 R.1.2" hardware distributed
by Futura Group srl or a compatible hardware.

**********************************************************************************


**********************************************************************************
Install:

To install the library use the command:

sudo python setup.py install

**********************************************************************************


**********************************************************************************
How to import library in your sketch? At the head of the file it is necessary
write this code

import sys
sys.path.insert(0, "/usr/local/lib/python2.7/dist-packages/MCP79410")
import MCP79410

**********************************************************************************
