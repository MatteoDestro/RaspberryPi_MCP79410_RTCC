#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#  Copyright 2015 root <root@RaspTest>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#====================================================================================================

#====================================================================================================
#  HISTORY
#  v1.0  -  First Release
#
#  =============================================================================
#  This is an example that shows how to set TimeKeeper and the alarms 0 and 1 of the MCP79410 device (RTCC - Real Time Clock Calendar).
#  The hardware used is referred to "shield RTCC MCP79410 Rev. 1.2" or higher developed by Futura Elettronica srl
#
#  Developed by Matteo Destro for Futura Group srl
#
#  www.Futurashop.it
#  www.open-electronics.org
#
#  BSD license, all text above must be included in any redistribution
#
#  The code for this demo is splitted into three files:
#
#  - MCP79410_SetAndReadRegisters -> Main file project
#  - MCP79410_PrintFunc           -> Contains code to print registers data read from MCP79410
#  - MCP79410_SetRegisters        -> Contains code to set registers (TimeKeeper and Alarm 0/1)
#
#  RaspberryPi 2.0/B+
#   
#  =============================================================================                    
#  
#  TO START EXAMPLE CODE
#  Type "sudo python MCP79410_SetAndReadRegisters.py" to start python code
#
#  SUPPORT
#  
#  info@open-electronics.org
#
#====================================================================================================

import time
import os
import sys
sys.path.insert(0, "/usr/local/lib/python2.7/dist-packages/MCP79410")
import RPi.GPIO as GPIO
import MCP79410
import threading
from   threading import Timer

from MCP79410_PrintFunc import *
from MCP79410_SetRegisters import *

#==========================================================
#	Global Var
NoCheckFlag   = False
NoPrintData	  = False
StopTimer     = False
PrintDataRead = False
#==========================================================

#==========================================================
#	Define pin
PULSE_P1  		= 27	#	Input - P1 Button -> Sets Date And Time
PULSE_P2  		= 18	#	Input - P2 Button -> Sets Alarm 0 and 1
PULSE_P3  		= 17	#	Input - P3 Button -> Reset Alarm 0 and 1

TRIG_1          = 22	#	Output - Debug Trigger 1
TRIG_2          = 23	#	Output - Debug Trigger 2
FORCE_ON        = 24 	#	Output - Line to forceOn Power Supply
LED_DIAGNOSTIC  = 25	#	Output - Diagnostic Led
#==========================================================

#==========================================================
#	GPIO Settings
GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom

GPIO.setup(PULSE_P1, GPIO.IN, pull_up_down=GPIO.PUD_UP)			# Pulsante P1
GPIO.setup(PULSE_P2, GPIO.IN, pull_up_down=GPIO.PUD_UP)			# Pulsante P2
GPIO.setup(PULSE_P3, GPIO.IN, pull_up_down=GPIO.PUD_UP)			# Pulsante P3

GPIO.setup(TRIG_1, GPIO.OUT, initial=GPIO.LOW) 					# Trigger 1
GPIO.setup(TRIG_2, GPIO.OUT, initial=GPIO.LOW) 					# Trigger 2
GPIO.setup(FORCE_ON, GPIO.OUT, initial=GPIO.LOW) 				# Force ON
GPIO.setup(LED_DIAGNOSTIC, GPIO.OUT, initial=GPIO.HIGH) 		# Led

GPIO.add_event_detect(PULSE_P1, GPIO.FALLING, bouncetime=100)
GPIO.add_event_detect(PULSE_P2, GPIO.FALLING, bouncetime=100)
GPIO.add_event_detect(PULSE_P3, GPIO.FALLING, bouncetime=100)
#==========================================================

#=================================================================== 
#	Timer 1 - This function is executed every 5 seconds
#	This function is used to read the registers of the MCP79410 and
#	after the data have been decoded the function procede to print
#	all on the screen   
def ReadsAndPrintsRegisters():
	global StopTimer
	global PrintDataRead
	global NoPrintData
	
	if (StopTimer == False):        			# If false restart timer
		threading.Timer(5.0, ReadsAndPrintsRegisters).start()
		
	if (NoPrintData == False):					# If false executes code below			
		NoCheckFlag = True
		MCP79410.ReadTimeKeeping()				#	Reads TimeKeeper registers
		MCP79410._CtrlReg.ControlByte.Byte0 = MCP79410.ReadSingleReg(MCP79410.RTCC_HW_ADD, MCP79410.CONTROL_ADD)
		MCP79410.ReadAlarmRegister(0)			#	Reads Alarm 0 configs
		MCP79410.ReadAlarmRegister(1)			#	Reads Alarm 1 configs
		if (MCP79410._TimeKeeper.WeekDay.WkDayBit.PwrFail == 1):
			MCP79410.ReadPowerDownUpRegister(0)	#	Reads PowerUp TimeStamp
			MCP79410.ReadPowerDownUpRegister(1)	#	Reads PowerDown TimeStamp
			MCP79410.ResetPwFailBit()
		PrintDataRead = True
		NoCheckFlag   = False
#===================================================================
	
#===================================================================      
#	Timer 2 - This function is executed every 1 second
#	Is usefull to verify the status of the alarms
#	In this script the Alarm 0 is used to PowerUp the Raspberry and
#	the Alarm 1 is used to PowerDown the Raspberry
def CheckAlarmsFlag():
	global StopTimer
	global NoCheckFlag
		
	if (NoCheckFlag == False):
		if (MCP79410._Alarm.Alm[0].WeekDay.WkDayBit.AlarmIF == 1):
			#	Power ON
			NoPrintData = True
			GPIO.output(FORCE_ON, GPIO.HIGH)	#	Force Power Supply ON
			time.sleep(.250)					#	Delay 250mSec
			MCP79410.Alarm0Bit(0)				#	Disable Alarm 0
			MCP79410.Alarm1Bit(1)				#	Enable  Alarm 1
			MCP79410.ResetAlarmIntFlagBit(0)	#	Reset   Alarm 0 Flag
			NoPrintData = False
		
		if (MCP79410._Alarm.Alm[1].WeekDay.WkDayBit.AlarmIF == 1):	
			#	Power OFF
			NoPrintData = True
			MCP79410.Alarm0Bit(1)				#	Enable  Alarm 0
			MCP79410.Alarm1Bit(0)				#	Disable Alarm 1
			MCP79410.ResetAlarmIntFlagBit(1)	#	Reset   Alarm 1 Flag
			time.sleep(2)
			os.system("sudo shutdown -h now")
			
	if (StopTimer == False):        			# If false restart timer
		threading.Timer(1.0, CheckAlarmsFlag).start()
#===================================================================      
		
def main():
	global StopTimer
	global PrintDataRead
		
	#=====================================
	#	Read EEPROM string "ElettronicaIn"
	MCP79410.ReadArray(MCP79410.EEPROM_HW_ADD, 0, 13)
	TempStr = ""
	for i in range(13):
		TempStr += chr(MCP79410.DataArray[i])
	
	print("\n#=============================================")
	print("Data read from EEPROM:")
	print(TempStr)
	print("#=============================================\n")
	#=====================================
	
	#====================================
	#	Starts Timers
	ReadsAndPrintsRegisters()	#	Starts timer to print registers value read from MCP79410
	CheckAlarmsFlag()			#	Starts timer to check Alarms flag
	#====================================
	
	while True:
		if (PrintDataRead == True):		#	If True prints data read from MCP79410 registers
			PrintDataRead = False		
			PrintDataMCP79410(True, True, True, True, True)		#	Recalls function tu print data read

		if GPIO.event_detected(PULSE_P1):
			#	Sets TimeKeeper registers
			print("P1 pulse intercepted. Sets TimeKeeper")
			NoPrintData = True
			NoCheckFlag = True
			SetTimeKeeperByLocalDateTime("24H")		#	Set Time and Date in 24H format
			NoPrintData = False
			NoCheckFlag = False

		if GPIO.event_detected(PULSE_P2):
			#	Sets Alarm registers
			print("P2 pulse intercepted. Sets Alarms")
			NoPrintData = True
			NoCheckFlag = True
			ManualSetAlarm0(0, 12, 40, 00, "24H", "AM", 25, 12, 1, 1, "LHL")
			ManualSetAlarm0(1, 12, 45, 00, "24H", "AM", 25, 12, 1, 1, "LHL")
			NoPrintData = False
			NoCheckFlag = False
			
		if GPIO.event_detected(PULSE_P3):
			print("P3 pulse intercepted. Reset Alarm")
			MCP79410.Alarm0Bit(0)				#	Disable Alarm 0
			MCP79410.Alarm1Bit(0)				#	Disable Alarm 1
			MCP79410.ResetAlarmIntFlagBit(0)	#	Reset Alarm 0
			MCP79410.ResetAlarmIntFlagBit(1)	#	Reset Alarm 1
			
			#GPIO.cleanup()
			#StopTimer = True
			#os.system("sudo shutdown -h now")
			return 0
							
	GPIO.cleanup()	
	return 0

if __name__ == '__main__':
	main()








