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
 

import MCP79410
import time

#===================================================================
#	This function sets Time and Date manually
#	The user must insert desired values
#	Hours       -> Inserts value from 0 to 23 
#	Minutes     -> Inserts value from 0 to 59 
#	Seconds     -> Inserts value from 0 to 59 
#	Set_12H_24H -> Insert string "12H" (Hour format 12H) or "24H" (Hour format 24H)
#	Set_AM_PM   -> Insert string "AM" or "PM"
#	Date        -> Inserts value from 1 to 31 
#	Month       -> Inserts value from 1 to 12
#	Year        -> Inserts value from 0 to 99 
#	WkDay       -> Inserts value from 0 to 6 (0 Sunday - 1 Monday etc)
def ManualSetTimeKeeper(Hours, Minutes, Seconds, Set_12H_24H, Set_AM_PM, Date, Month, Year, WkDay):
	MCP79410._TimeKeeper.Date.DateBit.DateOne    = (Date % 10)
	MCP79410._TimeKeeper.Date.DateBit.DateTen    = (Date / 10)
	MCP79410._TimeKeeper.Month.MonthBit.MonthOne = (Month % 10)
	MCP79410._TimeKeeper.Month.MonthBit.MonthTen = (Month / 10)
	MCP79410._TimeKeeper.Year.YearBit.YearOne    = (Year % 10)
	MCP79410._TimeKeeper.Year.YearBit.YearTen    = (Year / 10)
	MCP79410._TimeKeeper.WeekDay.WkDayBit.WkDay  = WkDay
	if (MCP79410._TimeKeeper.WeekDay.WkDayBit.WkDay == 0):	#	If "0" Sunday. Sets WkDay to "7"
		MCP79410._TimeKeeper.WeekDay.WkDayBit.WkDay = 7
		
	if (Set_12H_24H == "12H"):
		MCP79410._TimeKeeper.Hours24.Hour_12Byte.Byte0 = 0
		MCP79410._TimeKeeper.Hours12.Hour_12Bit._12_24 = 1
		if (Set_AM_PM == "AM"):
			MCP79410._TimeKeeper.Hours12.Hour_12Bit.AmPm = 0
		elif (Set_AM_PM == "PM"):	
			MCP79410._TimeKeeper.Hours12.Hour_12Bit.AmPm = 1
		else:
			print("Set AM/PM invalid parameter")			
		MCP79410._TimeKeeper.Hours12.Hour_12Bit.HrOne  = (Hours % 10)
		MCP79410._TimeKeeper.Hours12.Hour_12Bit.HrTen  = (Hours / 10)
	elif (Set_12H_24H == "24H"):
		MCP79410._TimeKeeper.Hours24.Hour_24Byte.Byte0 = 0
		MCP79410._TimeKeeper.Hours24.Hour_24Bit._12_24 = 0
		MCP79410._TimeKeeper.Hours24.Hour_24Bit.HrOne  = (Hours % 10)
		MCP79410._TimeKeeper.Hours24.Hour_24Bit.HrTen  = (Hours / 10)
	else:
		print("Set 12H/24H invalid parameter")
		
	MCP79410._TimeKeeper.Minutes.MinBit.MinOne     = (Minutes % 10)
	MCP79410._TimeKeeper.Minutes.MinBit.MinTen     = (Minutes / 10)
	MCP79410._TimeKeeper.Seconds.SecBit.SecOne     = (Seconds % 10)
	MCP79410._TimeKeeper.Seconds.SecBit.SecTen     = (Seconds / 10)
  
	MCP79410._TimeKeeper.Seconds.SecBit.StartOsc  = 1	# Start Oscillator
	MCP79410._TimeKeeper.WeekDay.WkDayBit.VbatEn  = 1	# Enable battery supply
  
	if (Set_12H_24H == "12H"):
		MCP79410.WriteTimeKeeping(1)	#  Set Date and Time. Time in 12H format
	elif (Set_12H_24H == "24H"):
		MCP79410.WriteTimeKeeping(0)	#  Set Date and Time. Time in 24H format
	else:
		print("Set 12H/24H invalid parameter")
#===================================================================

#===================================================================    	
#	This function sets Time and Date using the "Time" library
#	If "Set_12H_24H" = "12H" -> sets the 12H Format
#	If "Set_12H_24H" = "24H" -> sets the 24H Format
def SetTimeKeeperByLocalDateTime(Set_12H_24H):
	MCP79410._TimeKeeper.Date.DateBit.DateOne    = (int(time.strftime("%d")) % 10)
	MCP79410._TimeKeeper.Date.DateBit.DateTen    = (int(time.strftime("%d")) / 10) 
	MCP79410._TimeKeeper.Month.MonthBit.MonthOne = (int(time.strftime("%m")) % 10)
	MCP79410._TimeKeeper.Month.MonthBit.MonthTen = (int(time.strftime("%m")) / 10)
	MCP79410._TimeKeeper.Year.YearBit.YearOne    = (int(time.strftime("%y")) % 10)
	MCP79410._TimeKeeper.Year.YearBit.YearTen    = (int(time.strftime("%y")) / 10)
	MCP79410._TimeKeeper.WeekDay.WkDayBit.WkDay  = int(time.strftime("%w"))
	if (MCP79410._TimeKeeper.WeekDay.WkDayBit.WkDay == 0):	#	If "0" Sunday. Sets WkDay to "7"
		MCP79410._TimeKeeper.WeekDay.WkDayBit.WkDay = 7
  
	if (Set_12H_24H == "12H"):
		MCP79410._TimeKeeper.Hours24.Hour_12Byte.Byte0 = 0
		MCP79410._TimeKeeper.Hours12.Hour_12Bit._12_24 = 1
		if (time.strftime("%p") == "AM"):
			MCP79410._TimeKeeper.Hours12.Hour_12Bit.AmPm = 0
		elif (time.strftime("%p") == "PM"):
			MCP79410._TimeKeeper.Hours12.Hour_12Bit.AmPm = 1
		else:
			print("Set AM/PM invalid parameter")
		MCP79410._TimeKeeper.Hours12.Hour_12Bit.HrOne = (int(time.strftime("%H")) % 10)
		MCP79410._TimeKeeper.Hours12.Hour_12Bit.HrTen = (int(time.strftime("%H")) / 10) 		
	elif (Set_12H_24H == "24H"):
		MCP79410._TimeKeeper.Hours24.Hour_24Byte.Byte0 = 0
		MCP79410._TimeKeeper.Hours24.Hour_24Bit._12_24 = 0
		MCP79410._TimeKeeper.Hours24.Hour_24Bit.HrOne  = (int(time.strftime("%H")) % 10)
		MCP79410._TimeKeeper.Hours24.Hour_24Bit.HrTen  = (int(time.strftime("%H")) / 10) 	
	else:
		print("Set 12H/24H invalid parameter")
		
	MCP79410._TimeKeeper.Minutes.MinBit.MinOne     = (int(time.strftime("%M")) % 10) 
	MCP79410._TimeKeeper.Minutes.MinBit.MinTen     = (int(time.strftime("%M")) / 10) 
	MCP79410._TimeKeeper.Seconds.SecBit.SecOne     = (int(time.strftime("%S")) % 10)
	MCP79410._TimeKeeper.Seconds.SecBit.SecTen     = (int(time.strftime("%S")) / 10) 
  
	MCP79410._TimeKeeper.Seconds.SecBit.StartOsc  = 1	# Start Oscillator
	MCP79410._TimeKeeper.WeekDay.WkDayBit.VbatEn  = 1	# Enable battery supply

	if (Set_12H_24H == "12H"):
		MCP79410.WriteTimeKeeping(1)	#  Set Date and Time. Time in 12H format
	elif (Set_12H_24H == "24H"):
		MCP79410.WriteTimeKeeping(0)	#  Set Date and Time. Time in 24H format
	else:
		print("Set 12H/24H invalid parameter")
#===================================================================

#===================================================================
#	This function sets Alarm 0 or 1
#	If Index = 0 -> Sets Alarm 0
#	If Index = 1 -> Sets Alarm 1
#	Hours       -> Inserts value from 0 to 23 
#	Minutes     -> Inserts value from 0 to 59 
#	Seconds     -> Inserts value from 0 to 59 
#	Set_12H_24H -> Insert string "12H" (Hour format 12H) or "24H" (Hour format 24H)
#	Set_AM_PM   -> Insert string "AM" or "PM"
#	Date        -> Inserts value from 1 to 31 
#	Month       -> Inserts value from 1 to 12 
#	WkDay       -> Inserts value from 0 to 6 (0 Sunday - 1 Monday etc)
#   AlarmMask   -> Insert value from 0 to 7
#                  If "0"         -> Seconds Match
#                  If "1"         -> Minutes Match
#                  If "2"         -> Hours Match
#                  If "3"         -> Day Of Week Match
#                  If "4"         -> Date Match
#                  If "5" And "6" -> Reserved
#                  If "7"         -> All Match
#	AlarmPol    -> Insert string "LHL" (Logic High Level) or "LLL" (Logic Low Level)
def ManualSetAlarm0(Index, Hours, Minutes, Seconds, Set_12H_24H, Set_AM_PM, Date, Month, WkDay, AlarmMask, AlarmPol):
	if (Index == 0):
		MCP79410.Alarm0Bit(0)	#	Disable Alarm 0
	else:
		MCP79410.Alarm1Bit(0)	#	Disable Alarm 1
		
	MCP79410._Alarm.Alm[Index].Date.DateBit.DateOne       = (Date % 10)
	MCP79410._Alarm.Alm[Index].Date.DateBit.DateTen       = (Date / 10)
	MCP79410._Alarm.Alm[Index].Month.MonthBit.MonthOne    = (Month % 10)
	MCP79410._Alarm.Alm[Index].Month.MonthBit.MonthTen    = (Month / 10)
	MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.WkDay     = WkDay
	if (MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.WkDay == 0):
		MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.WkDay = 7
		
	MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.AlarmMask = AlarmMask
	
	if (AlarmPol == "LHL"):
		MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.AlarmPol = 1	#	LHL - Logic High Level
	elif (AlarmPol == "LLL"):
		MCP79410._Alarm.Alm[Index].WeekDay.WkDayBit.AlarmPol = 0	#	LLL - Logic Low Level
	else:
		print("Set AlarmPol invalid parameter")
		
	if (Set_12H_24H == "12H"):
		MCP79410._Alarm.Alm[Index].Hours12.Hour_12Byte.Byte0 = 0
		MCP79410._Alarm.Alm[Index].Hours12.Hour_12Bit._12_24 = 1
		if (Set_AM_PM == "AM"):
			MCP79410._Alarm.Alm[Index].Hours12.Hour_12Bit.AmPm = 0
		elif (Set_AM_PM == "PM"):
			MCP79410._Alarm.Alm[Index].Hours12.Hour_12Bit.AmPm = 1
		else:
			print("Set AM/PM invalid parameter")	
		MCP79410._Alarm.Alm[Index].Hours12.Hour_12Bit.HrOne = (Hours % 10)
		MCP79410._Alarm.Alm[Index].Hours12.Hour_12Bit.HrTen = (Hours / 10)
	elif (Set_12H_24H == "24H"):
		MCP79410._Alarm.Alm[Index].Hours24.Hour_24Byte.Byte0 = 0
		MCP79410._Alarm.Alm[Index].Hours24.Hour_24Bit._12_24 = 0
		MCP79410._Alarm.Alm[Index].Hours24.Hour_24Bit.HrOne  = (Hours % 10)
		MCP79410._Alarm.Alm[Index].Hours24.Hour_24Bit.HrTen  = (Hours / 10)
	else:
		print("Set 12H/24H invalid parameter")
		
	MCP79410._Alarm.Alm[Index].Minutes.MinBit.MinOne = (Minutes % 10)
	MCP79410._Alarm.Alm[Index].Minutes.MinBit.MinTen = (Minutes / 10) 
	MCP79410._Alarm.Alm[Index].Seconds.SecBit.SecOne = (Seconds % 10)
	MCP79410._Alarm.Alm[Index].Seconds.SecBit.SecTen = (Seconds / 10)
       
	if (Set_12H_24H == "12H"):
		MCP79410.WriteAlarmRegister(Index, 1)
	elif (Set_12H_24H == "24H"):
		MCP79410.WriteAlarmRegister(Index, 0)
	else:
		print("Set 12H/24H invalid parameter")
		
	if (Index == 0):
		MCP79410.Alarm0Bit(1)                #  Enable Alarm 0
	else:
		MCP79410.Alarm1Bit(1)                #  Enable Alarm 1
#===================================================================
	
