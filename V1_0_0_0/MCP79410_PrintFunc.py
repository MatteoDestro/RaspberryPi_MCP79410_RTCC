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
 

import sys
import MCP79410

#======================================================================
#   This function generate a string with the time registers read from MCP79410
#	If WhichParameter = 0 -> Works with TimeKeeper registers
#	If WhichParameter = 1 -> Works with Alarm registers (Alarm 0/1)
#	If WhichParameter = 2 -> Works with TimeStamp registers (Power Down/Up)
#	If Index = 0 -> Works with Alarm 0 (WhichParameter = 1) or with TimeStamp PowerUp (WhichParameter = 2)
#	If Index = 1 -> Works with Alarm 1 (WhichParameter = 1) or with TimeStamp PowerDown (WhichParameter = 2)
def PrintTime(WhichParameter, Index):
	TempStr  = ""
	if (WhichParameter == 0):
		#	Print TimeKeeper Time
		TempStr  = chr(MCP79410._TimeKeeper.Hours24.Hour_24Bit.HrTen + 0x30)
		TempStr += chr(MCP79410._TimeKeeper.Hours24.Hour_24Bit.HrOne + 0x30)
		TempStr += ":"
		TempStr += chr(MCP79410._TimeKeeper.Minutes.MinBit.MinTen + 0x30)
		TempStr += chr(MCP79410._TimeKeeper.Minutes.MinBit.MinOne + 0x30)
		TempStr += ":"
		TempStr += chr(MCP79410._TimeKeeper.Seconds.SecBit.SecTen + 0x30)
		TempStr += chr(MCP79410._TimeKeeper.Seconds.SecBit.SecOne + 0x30)
		if (MCP79410._TimeKeeper.Hours24.Hour_24Bit._12_24 == 0):
			#  24H format 
			TempStr += ""
		else:
			#  12H format
			if (MCP79410._TimeKeeper.Hours12.Hour_12Bit.AmPm == 0):
				#  AM
				TempStr += " - AM"
			else:
				#  PM
				TempStr += " - PM"
	elif (WhichParameter == 1):
		#	Print Alarm Time
		TempStr  = chr(MCP79410._Alarm.Alm[Index].Hours24.Hour_24Bit.HrTen + 0x30)
		TempStr += chr(MCP79410._Alarm.Alm[Index].Hours24.Hour_24Bit.HrOne + 0x30)
		TempStr += ":"
		TempStr += chr(MCP79410._Alarm.Alm[Index].Minutes.MinBit.MinTen + 0x30)
		TempStr += chr(MCP79410._Alarm.Alm[Index].Minutes.MinBit.MinOne + 0x30)
		TempStr += ":"
		TempStr += chr(MCP79410._Alarm.Alm[Index].Seconds.SecBit.SecTen + 0x30)
		TempStr += chr(MCP79410._Alarm.Alm[Index].Seconds.SecBit.SecOne + 0x30)
		if (MCP79410._Alarm.Alm[Index].Hours24.Hour_24Bit._12_24 == 0):
			#  24H format 
			TempStr += ""
		else:
			#  12H format
			if (MCP79410._Alarm.Alm[Index].Hours12.Hour_12Bit.AmPm == 0):
				#  AM
				TempStr += " - AM"
			else:
				#  PM
				TempStr += " - PM"		
	elif (WhichParameter == 2):
		#	Print PowerStamp Time
		TempStr  = chr(MCP79410._PwrTimeStamp.Pwr[Index].Hours24.Hour_24Bit.HrTen + 0x30)
		TempStr += chr(MCP79410._PwrTimeStamp.Pwr[Index].Hours24.Hour_24Bit.HrOne + 0x30)
		TempStr += ":"
		TempStr += chr(MCP79410._PwrTimeStamp.Pwr[Index].Minutes.MinBit.MinTen + 0x30)
		TempStr += chr(MCP79410._PwrTimeStamp.Pwr[Index].Minutes.MinBit.MinOne + 0x30)
		TempStr += ":XX"
		if (MCP79410._PwrTimeStamp.Pwr[Index].Hours24.Hour_24Bit._12_24 == 0):
			#  24H format 
			TempStr += " -> "
		else:
			#  12H format
			if (MCP79410._PwrTimeStamp.Pwr[Index].Hours12.Hour_12Bit.AmPm == 0):
				#  AM
				TempStr += " AM -> "
			else:
				#  PM
				TempStr += " PM -> "
		return(TempStr)			
	else:
		TempStr  = "Parameter Error"
	return(TempStr + "\n")
#======================================================================

#======================================================================
#   This function generate a string with the Date registers read from MCP79410
#	If WhichParameter = 0 -> Works with TimeKeeper registers
#	If WhichParameter = 1 -> Works with Alarm registers (Alarm 0/1)
#	If WhichParameter = 2 -> Works with TimeStamp registers (Power Down/Up)
#	If Index = 0 -> Works with Alarm 0 (WhichParameter = 1) or with TimeStamp PowerUp (WhichParameter = 2)
#	If Index = 1 -> Works with Alarm 1 (WhichParameter = 1) or with TimeStamp PowerDown (WhichParameter = 2)
def PrintDate(WhichParameter, Index):
	TempStr  = ""
	if (WhichParameter == 0):
		TempData = MCP79410._TimeKeeper.WeekDay.WkDayBit.WkDay
		TempStr += chr(MCP79410._TimeKeeper.Date.DateBit.DateTen + 0x30)
		TempStr += chr(MCP79410._TimeKeeper.Date.DateBit.DateOne + 0x30)
		TempStr += "/"
		TempStr += chr(MCP79410._TimeKeeper.Month.MonthBit.MonthTen + 0x30)
		TempStr += chr(MCP79410._TimeKeeper.Month.MonthBit.MonthOne + 0x30)
		TempStr += "/"
		TempStr += "20"
		TempStr += chr(MCP79410._TimeKeeper.Year.YearBit.YearTen + 0x30)
		TempStr += chr(MCP79410._TimeKeeper.Year.YearBit.YearOne + 0x30) 
		TempStr += " - "
	elif (WhichParameter == 1):
		TempData = MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.WkDay
		TempStr += chr(MCP79410._Alarm.Alm[Index].Date.DateBit.DateTen + 0x30)
		TempStr += chr(MCP79410._Alarm.Alm[Index].Date.DateBit.DateOne + 0x30)
		TempStr += "/"
		TempStr += chr(MCP79410._Alarm.Alm[Index].Month.MonthBit.MonthTen + 0x30)
		TempStr += chr(MCP79410._Alarm.Alm[Index].Month.MonthBit.MonthOne + 0x30)
		TempStr += "/YYYY - "
	elif (WhichParameter == 2):
		TempData = MCP79410._PwrTimeStamp.Pwr[Index].Month.MonthBit.WkDay
		TempStr += chr(MCP79410._PwrTimeStamp.Pwr[Index].Date.DateBit.DateTen + 0x30)
		TempStr += chr(MCP79410._PwrTimeStamp.Pwr[Index].Date.DateBit.DateOne + 0x30)
		TempStr += "/"
		TempStr += chr(MCP79410._PwrTimeStamp.Pwr[Index].Month.MonthBit.MonthTen + 0x30)
		TempStr += chr(MCP79410._PwrTimeStamp.Pwr[Index].Month.MonthBit.MonthOne + 0x30)
		TempStr += "/YYYY - "
	else:
		TempStr  = "Parameter Error"
	   
	if (TempData == 1):
		#	Monday
		TempStr += "MON\n"
	elif (TempData == 2):
		#	Tuesday
		TempStr += "TUE\n"
	elif (TempData == 3):
		#	Wednesday
		TempStr += "WED\n"
	elif (TempData == 4):
		#	Thursday
		TempStr += "THU\n"
	elif (TempData == 5):
		#	Friday
		TempStr += "FRI\n"
	elif (TempData == 6):
		#	Saturday
		TempStr += "SAT\n"
	elif (TempData == 7):
		#	Sunday
		TempStr += "SUN\n"
	else:
		if (WhichParameter == 2):
			TempStr += "***"
		else:
			TempStr += "***\n"
		
	if (WhichParameter == 1):
		TempStr += "# Alarm Mask Set        -> "
		TempData = MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.AlarmMask 
		if (TempData == 0):
			#  Seconds Match
			TempStr += "SecondsMatch"
		elif (TempData == 1):    
			#  Minutes Match
			TempStr += "MinutesMatch"
		elif (TempData == 2):    
			#  Hours Match
			TempStr += "HoursMatch"
		elif (TempData == 3):    
			#  Day Of The Week Match
			TempStr += "DayOfWeekMatch"
		elif (TempData == 4):       
			#  Date Match						
			TempStr += "DateMatch"
		elif (TempData == 7):          
			#  All Match
			TempStr += "AllMatch"
		else:
			TempStr += "# Alarm Mask config Error"
			
	return (TempStr + "\n")
#======================================================================

#======================================================================
#	This function prints data read from MCP79410
#	if PrintTimeKeeper = True -> Print TimeKeeper registers
#	if PrintAlarm0     = True -> Print Alarm 0 registers
#	if PrintAlarm1     = True -> Print Alarm 1 registers
#	if PrintPowerDown  = True -> Print PowerDown TimeStamp registers
#	if PrintPowerUp    = True -> Print PowerUp TimeStamp registers
def PrintDataMCP79410(PrintTimeKeeper, PrintAlarm0, PrintAlarm1, PrintPowerDown, PrintPowerUp):
	print("#=================================================================")	
	if (MCP79410._TimeKeeper.WeekDay.WkDayBit.OSCrun != 0):
		if (PrintTimeKeeper == True):
			PrintTimeKeeper = False
			print("# Oscillator is enabled and running")
			sys.stdout.write("# Time Readed: " + PrintTime(0, 0))
			sys.stdout.write("# Date Readed: " + PrintDate(0 ,0))
		
		if (PrintAlarm0 == True):
			PrintAlarm0 = False
			#-----------------------------------------------------------
			#	Print Alarm 0 info
			print("\n#=============================================")
			sys.stdout.write("# Alarm 0 is            -> ")
			if (MCP79410._CtrlReg.ControlBit.Alarm0_Enable == 1):
				print("Enabled")
			else:
				print("Disabled")
			sys.stdout.write("# Alarm Output Polarity -> ")
			if (MCP79410._Alarm.Alm[0].WeekDay.WkDayBit.AlarmPol == 1):
				print("MFP is a logic high level")
			else:
				print("MFP is a logic low level")
			sys.stdout.write("# Alarm Interrupt Flag  -> ")
			if (MCP79410._Alarm.Alm[0].WeekDay.WkDayBit.AlarmIF == 1):
				print("1")
			else:
				print("0")
			sys.stdout.write("# Alarm time configured -> " + PrintTime(1, 0))
			sys.stdout.write("# Alarm date configured -> " + PrintDate(1 ,0))
			print("#=============================================")
			#-----------------------------------------------------------
			
		if (PrintAlarm1 == True):
			PrintAlarm1 = False		
			#-----------------------------------------------------------
			#	Print Alarm 1 info
			print("\n#=============================================")
			sys.stdout.write("# Alarm 1 is            -> ")
			if (MCP79410._CtrlReg.ControlBit.Alarm1_Enable == 1):
				print("Enabled")
			else:
				print("Disabled")
			sys.stdout.write("# Alarm Output Polarity -> ")
			if (MCP79410._Alarm.Alm[1].WeekDay.WkDayBit.AlarmPol == 1):
				print("MFP is a logic high level")
			else:
				print("MFP is a logic low level")
			sys.stdout.write("# Alarm Interrupt Flag  -> ")
			if (MCP79410._Alarm.Alm[1].WeekDay.WkDayBit.AlarmIF == 1):
				print("1")
			else:
				print("0")
			sys.stdout.write("# Alarm time configured -> " + PrintTime(1, 1))
			sys.stdout.write("# Alarm date configured -> " + PrintDate(1 ,1))
			print("#=============================================")
			#-----------------------------------------------------------
		
		if (PrintPowerDown == True):
			PrintPowerDown = False	
			#-----------------------------------------------------------
			#	Print PowerDown TimeStamp info
			print("\n#=============================================")
			sys.stdout.write("# TimeStamp PowerDown: " + PrintTime(2, 1) + PrintDate(2 ,1))
			print("#=============================================")
			#-----------------------------------------------------------
			
		if (PrintPowerUp == True):
			PrintPowerUp = False
			#-----------------------------------------------------------
			#	Print PowerUp TimeStamp info
			print("\n#=============================================")
			sys.stdout.write("# TimeStamp PowerUp:   " + PrintTime(2, 0) + PrintDate(2 ,0))
			print("#=============================================")				
			#-----------------------------------------------------------
	else:
		print("# Oscillator has stopped or has been disabled")
	print("#=================================================================\n")	
#======================================================================
