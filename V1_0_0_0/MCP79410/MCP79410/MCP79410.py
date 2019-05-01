#===========================================================================
#  This is the library for MCP79410 RTCC (Real Time Clock Calendar). 
#  
#  Written by Matteo Destro for Futura Group srl
#  www.Futurashop.it
#  www.open-electronics.org
# 
#  BSD license, all text above must be included in any redistribution
#  ===========================================================================
#
#	REVISION	1.0.0	27/12/2015
#
#  ===========================================================================
#
#  INSTALLATION
#  The library is composed by two files (MCP79410.py, MCP79410_DefVar.py)
#
#  SUPPORT
#
#  info@open-electronics.org
#
#===========================================================================

from ctypes import *
from MCP79410_DefVar import *

import smbus
import time
import sys

#I2Cbus = smbus.SMBus(0)
I2Cbus = smbus.SMBus(1)

_CtrlReg      = CtrlReg()
_TimeKeeper   = TimeKeeperStruct()	
_Alarm        = AlarmArray()
_PwrTimeStamp = PowerArray()

#======================================================================================================================================
#==============================
#	GENERAL PURPOSE FUNCTIONS
#==============================
#===================================================================
#	This function toggles a single bit into selected register
#	ControlByte = Hardware address + W/R bit
#	RegAdd      = Register address
#	Bit         = Bit to set
def ToggleSingleBit(ControlByte, RegAdd, Bit):
	if (Bit > 7):
		Bit = 7
	try:
		DataRead = I2Cbus.read_byte_data(ControlByte, RegAdd)
		DataRead ^= (0x01 << Bit)
		I2Cbus.write_byte_data(ControlByte, RegAdd, DataRead)
	except:
		print("I2C error occurred - ToggleSingleBit")
		pass
#===================================================================

#===================================================================
#	This function sets a single bit into selected register
#	ControlByte = Hardware address + W/R bit
#	RegAdd      = Register address
#	Bit         = Bit to set
def SetSingleBit(ControlByte, RegAdd, Bit):
	if (Bit > 7):
		Bit = 7
	
	try:
		DataRead = I2Cbus.read_byte_data(ControlByte, RegAdd)
		DataRead |= (0x01 << Bit)
		I2Cbus.write_byte_data(ControlByte, RegAdd, DataRead)
	except:
		print("I2C error occurred - SetSingleBit")
		pass
#===================================================================

#===================================================================
#	This function resets a single bit into selected register
#	ControlByte = Hardware address + W/R bit
#	RegAdd      = Register address
#	Bit         = Bit to reset
def ResetSingleBit(ControlByte, RegAdd, Bit):
	if (Bit > 7):
		Bit = 7

	try:		
		DataRead = I2Cbus.read_byte_data(ControlByte, RegAdd)
		DataRead &= ~(0x01 << Bit)
		I2Cbus.write_byte_data(ControlByte, RegAdd, DataRead)
	except:
		print("I2C error occurred - ResetSingleBit")
		pass
#===================================================================

#===================================================================
#	This function writes a single register
#	ControlByte = Hardware address + W/R bit
#	RegAdd      = Register address
#	RegData     = Data to write into register selected
def WriteSingleReg(ControlByte, RegAdd, RegData):
	try:
		I2Cbus.write_byte_data(ControlByte, RegAdd, RegData)
	except:
		print("I2C error occurred - WriteSingleReg")
		pass
#===================================================================

#===================================================================
#	This function writes n bytes sequentially
#	For internal EEPROM max 8 Byte at once
#	ControlByte = Hardware address + W/R bit
#	StartAdd    = Start Address to write
#	Lenght      = n Byte to write
def WriteArray(ControlByte, StartAdd, Lenght):
	global DataArray
	_DataTemp = c_ubyte * (Lenght + 1)
	
	for i in range(Lenght):
		_DataTemp[i] = DataArray[i]
		
	try:
		I2Cbus.write_i2c_block_data(ControlByte, StartAdd, _DataTemp)
	except:
		print("I2C error occurred - WriteArray")
		pass
#===================================================================

#===================================================================
#	This function clear a single register
#	ControlByte = Hardware address + W/R bit
#	RegAdd      = Register address
def ClearReg(ControlByte, RegAdd):
	try:
		I2Cbus.write_byte_data(ControlByte, RegAdd, 0x00)
	except:
		print("I2C error occurred - ClearReg")
		pass
#===================================================================

#===================================================================
#	This function read a single register
# 	ControlByte = Hardware address + W/R bit
#   RegAdd      = Register address
#	This function return the value of selected register
def ReadSingleReg(ControlByte, RegAdd):
	try:
		return(I2Cbus.read_byte_data(ControlByte, RegAdd))
	except:
		print("I2C error occurred - ReadSingleReg")
		pass
		return(0)	
#===================================================================

#===================================================================
#	This function read n bytes sequentially
#	ControlByte = Hardware address + W/R bit
#	StartAdd    = Start Address to read
#	Lenght      = n Byte to read
def ReadArray(ControlByte, StartAdd, Lenght):
	global DataArray
	
	try:
		DataArray = I2Cbus.read_i2c_block_data(ControlByte, StartAdd, Lenght)
	except:
		print("I2C error occurred - ReadArray")
		pass		
#===================================================================
#======================================================================================================================================


#======================================================================================================================================
#==============================
#	RTCC DEDICATED FUNCTIONS
#==============================

#===================================================================
#	This function Set/Reset OUT Bit in CONTROL register
#	SetReset => "1" Set; "0" Reset
def GeneralPurposeOutputBit(SetReset):
	if (SetReset != 0):
		SetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 7)
	else:
		ResetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 7)
#===================================================================	

#===================================================================
#	This function Set/Reset SQWEN Bit in CONTROL register
#	EnableDisable => "1" Enable; "0" Disable	
def SquareWaveOutputBit(EnableDisable):
	if (EnableDisable != 0):
		SetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 6)
	else:
		ResetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 6)
#===================================================================	

#===================================================================	
#	This function Enable/Disable Alarm 1 in CONTROL register
#	EnableDisable => "1" Enable; "0" Disable
def Alarm1Bit(EnableDisable):
	if (EnableDisable != 0):
		SetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 5)
	else:
		ResetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 5)	
#===================================================================	
	
#===================================================================	
#	This function Enable/Disable Alarm 0 in CONTROL register
#	EnableDisable => "1" Enable; "0" Disable
def Alarm0Bit(EnableDisable):
	if (EnableDisable != 0):
		SetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 4)
	else:
		ResetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 4)	
#===================================================================	

#===================================================================	
#	This function Enable/Disable ExtOSC in CONTROL register
#	EnableDisable => "1" Enable; "0" Disable
def ExternalOscillatorBit(EnableDisable):
	if (EnableDisable != 0):
		SetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 3)
	else:
		ResetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 3)
#===================================================================	

#===================================================================	
#	This function Enable/Disable CRSTRIM in CONTROL register
#	EnableDisable => "1" Enable; "0" Disable
def CoarseTrimModeBit(EnableDisable):
	if (EnableDisable != 0):
		SetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 2)
	else:
		ResetSingleBit(RTCC_HW_ADD, CONTROL_ADD, 2)
#===================================================================	

#===================================================================	
#	This function Set SQWFS in CONTROL register
#	OutputFreq => 00 (0) -> 1 Hz
#   			  01 (1) -> 4096 Hz
# 			      10 (2) -> 8192 Hz
#	  		      11 (3) -> 32768 Hz
def SetOutputFrequencyBit(OutputFreq):
	RegData  = ReadSingleReg(RTCC_HW_ADD, CONTROL_ADD)
	RegData &= 0xFC;
	RegData |= OutputFreq;	
	WriteSingleReg(RTCC_HW_ADD, CONTROL_ADD, RegData)
#===================================================================	

	


#===================================================================	
#	This function Set/Reset Start Oscillator Bit in RTCSEC register
#	EnableDisable => "1" Enable; "0" Disable
def StartOscillatorBit(EnableDisable):
	if (EnableDisable != 0):
		SetSingleBit(RTCC_HW_ADD, RTCSEC_ADD, 7)
	else:
		ResetSingleBit(RTCC_HW_ADD, RTCSEC_ADD, 7)
#===================================================================	




#===================================================================	
#	This function Set 12 or 24 Hour Time Format Bit in RTCHOUR register
#	SetHourType => "1" 12 Hour; "0" 24 Hour
def Hour12or24TimeFormatBit(SetHourType):
	if (SetHourType != 0):
		SetSingleBit(RTCC_HW_ADD, RTCHOUR_ADD, 6)
	else:
		ResetSingleBit(RTCC_HW_ADD, RTCHOUR_ADD, 6)
#===================================================================	

#===================================================================
#	This function Set AM or PM Bit in RTCHOUR register
#	SetAmPm => "1" PM; "0" AM
def AmPmBit(SetAmPm):
	if (SetAmPm != 0):
		SetSingleBit(RTCC_HW_ADD, RTCHOUR_ADD, 5)
	else:
		ResetSingleBit(RTCC_HW_ADD, RTCHOUR_ADD, 5)
#===================================================================

#===================================================================
#	This function Set/Reset Vbaten Bit in RTCWKDAY register
#	EnableDisable => "1" Enable; "0" Disable
def VbatEnBit(EnableDisable):
	if (EnableDisable != 0):
		SetSingleBit(RTCC_HW_ADD, RTCWKDAY_ADD, 3)
	else:
		ResetSingleBit(RTCC_HW_ADD, RTCWKDAY_ADD, 3)
#===================================================================

#===================================================================
#	This function Reset PwFail Bit in RTCWKDAY register
def ResetPwFailBit():
	ResetSingleBit(RTCC_HW_ADD, RTCWKDAY_ADD, 4)
#===================================================================




#===================================================================
#	This function Set 12 or 24 Hour Time Format Bit in ALARMxHOUR register
#	SetHourType => "1" 12 Hour; "0" 24 Hour
#	Alarm0_1 => "1" Alarm 1; "0" Alarm 0
def AlarmHour12or24TimeFormatBit(SetHourType, Alarm0_1):
	if (SetHourType != 0):
		if (Alarm0_1 != 0):
			SetSingleBit(RTCC_HW_ADD, ALM1HOUR_ADD, 6)
		else:
			SetSingleBit(RTCC_HW_ADD, ALM0HOUR_ADD, 6)
	else:
		if (Alarm0_1 != 0):
			ResetSingleBit(RTCC_HW_ADD, ALM1HOUR_ADD, 6)
		else:
			ResetSingleBit(RTCC_HW_ADD, ALM0HOUR_ADD, 6)
#===================================================================

#===================================================================
#	This function Set AM or PM Bit in ALARMxHOUR register
#	SetAmPm => "1" PM; "0" AM
#	Alarm0_1 => "1" Alarm 1; "0" Alarm 0
def AlarmAmPmBit(SetAmPm, Alarm0_1):
	if (SetAmPm != 0):
		if (Alarm0_1 != 0):
			SetSingleBit(RTCC_HW_ADD, ALM1HOUR_ADD, 5)
		else:
			SetSingleBit(RTCC_HW_ADD, ALM0HOUR_ADD, 5)
	else:
		if (Alarm0_1 != 0):
			ResetSingleBit(RTCC_HW_ADD, ALM1HOUR_ADD, 5)
		else:
			ResetSingleBit(RTCC_HW_ADD, ALM0HOUR_ADD, 5)
#===================================================================

#===================================================================
#	This function Set/Reset ALMPOL Bit in ALARMxWKDAY register
#	SetReset => "1" Set; "0" Reset
#	Alarm0_1 => "1" Alarm 1; "0" Alarm 0
def AlarmIntOutputPolarityBit(SetReset, Alarm0_1):
	if (SetReset != 0):
		if (Alarm0_1 != 0):
			SetSingleBit(RTCC_HW_ADD, ALM1WKDAY_ADD, 7)
		else:
			SetSingleBit(RTCC_HW_ADD, ALM0WKDAY_ADD, 7)
	else:
		if (Alarm0_1 != 0):
			ResetSingleBit(RTCC_HW_ADD, ALM1WKDAY_ADD, 7)
		else:
			ResetSingleBit(RTCC_HW_ADD, ALM0WKDAY_ADD, 7)
#===================================================================

#===================================================================
#	This function Set ALMxMSK Bits in ALARMxWKDAY register
#	Alarm0_1 => "1" Alarm 1; "0" Alarm 0
#	Mask     => 000 (0) -> Seconds match
#               001 (1) -> Minutes match
# 			    010 (2) -> Hours match
#  		        011 (3) -> Day of week match
#               100 (4) -> Date match
#               101 (5) -> Reserved
#    		    110 (6) -> Reserved
# 			    111 (7) -> Seconds, Minutes, Hour, Day of Week, Date and Month match
def AlarmMaskBit(Alarm0_1, Mask):
	if (Alarm0_1 != 0):
		RegData = ReadSingleReg(RTCC_HW_ADD, ALM1WKDAY_ADD)
		RegData &= 0x8F
		RegData |= Mask
		WriteSingleReg(RTCC_HW_ADD, ALM1WKDAY_ADD, RegData)
	else:
		RegData = ReadSingleReg(RTCC_HW_ADD, ALM0WKDAY_ADD)
		RegData &= 0x8F
		RegData |= Mask
		WriteSingleReg(RTCC_HW_ADD, ALM0WKDAY_ADD, RegData)
#===================================================================

#===================================================================
#	This function Reset ALMxIF Bit in ALARMxWKDAY register
#	Alarm0_1 => "1" Alarm 1; "0" Alarm 0
def ResetAlarmIntFlagBit(Alarm0_1):
	if (Alarm0_1 != 0):
		ResetSingleBit(RTCC_HW_ADD, ALM1WKDAY_ADD, 3)
	else:
		ResetSingleBit(RTCC_HW_ADD, ALM0WKDAY_ADD, 3)
#===================================================================



#===================================================================
#	This function Set 12 or 24 Hour Time Format Bit in PWRxxHOUR register
#	SetHourType => "1" 12 Hour; "0" 24 Hour
#	PowerDownUp => "1" PowerDown; "0" PowerUp
def PowerHour12or24TimeFormatBit(SetHourType, PowerDownUp):
	if (SetHourType != 0):
		if (PowerDownUp != 0):
			SetSingleBit(RTCC_HW_ADD, PWRDWHOUR_ADD, 6)
		else:
			SetSingleBit(RTCC_HW_ADD, PWRUPHOUR_ADD, 6)
	else:
		if (PowerDownUp != 0):
			ResetSingleBit(RTCC_HW_ADD, PWRDWHOUR_ADD, 6)
		else:
			ResetSingleBit(RTCC_HW_ADD, PWRUPHOUR_ADD, 6)
#===================================================================

#===================================================================
#	This function Set AM or PM Bit in ALARMxHOUR register
#	SetAmPm => "1" PM; "0" AM
#	PowerDownUp => "1" PowerDown; "0" PowerUp
def PowerAmPmBit(SetAmPm, PowerDownUp):
	if (SetAmPm != 0):
		if (PowerDownUp != 0):
			SetSingleBit(RTCC_HW_ADD, PWRDWHOUR_ADD, 5)
		else:
			SetSingleBit(RTCC_HW_ADD, PWRUPHOUR_ADD, 5)
	else:
		if (PowerDownUp != 0):
			ResetSingleBit(RTCC_HW_ADD, PWRDWHOUR_ADD, 5)
		else:
			ResetSingleBit(RTCC_HW_ADD, PWRUPHOUR_ADD, 5)	
#===================================================================




#===================================================================
#	This function writes TimeKeeping registers
#	SetHourType => "1" 12-Hour Format; "0" 24-Hour Format
def WriteTimeKeeping(SetHourType):
	global _TimeKeeper
	
	WriteSingleReg(RTCC_HW_ADD, RTCSEC_ADD, _TimeKeeper.Seconds.SecByte.Byte0)
	WriteSingleReg(RTCC_HW_ADD, RTCMIN_ADD, _TimeKeeper.Minutes.MinByte.Byte0)
	if (SetHourType != 0):
		WriteSingleReg(RTCC_HW_ADD, RTCHOUR_ADD, _TimeKeeper.Hours12.Hour_12Byte.Byte0)
	else:
		WriteSingleReg(RTCC_HW_ADD, RTCHOUR_ADD, _TimeKeeper.Hours24.Hour_24Byte.Byte0)
	WriteSingleReg(RTCC_HW_ADD, RTCWKDAY_ADD, _TimeKeeper.WeekDay.WkDayByte.Byte0)
	WriteSingleReg(RTCC_HW_ADD, RTCDATE_ADD,  _TimeKeeper.Date.DateByte.Byte0)
	WriteSingleReg(RTCC_HW_ADD, RTCMTH_ADD,   _TimeKeeper.Month.MonthByte.Byte0)
	WriteSingleReg(RTCC_HW_ADD, RTCYEAR_ADD,  _TimeKeeper.Year.YearByte.Byte0)
#===================================================================

#===================================================================
#	This function reads TimeKeeping registers
def ReadTimeKeeping():
	global _TimeKeeper
	
	_TimeKeeper.Seconds.SecByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, RTCSEC_ADD)
	_TimeKeeper.Minutes.MinByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, RTCMIN_ADD)
	_TimeKeeper.Hours12.Hour_12Byte.Byte0 = ReadSingleReg(RTCC_HW_ADD, RTCHOUR_ADD)
	_TimeKeeper.Hours24.Hour_24Byte.Byte0 = _TimeKeeper.Hours12.Hour_12Byte.Byte0
	_TimeKeeper.WeekDay.WkDayByte.Byte0   = ReadSingleReg(RTCC_HW_ADD, RTCWKDAY_ADD)
	_TimeKeeper.Date.DateByte.Byte0       = ReadSingleReg(RTCC_HW_ADD, RTCDATE_ADD)
	_TimeKeeper.Month.MonthByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, RTCMTH_ADD)
	_TimeKeeper.Year.YearByte.Byte0       = ReadSingleReg(RTCC_HW_ADD, RTCYEAR_ADD)
#===================================================================



#===================================================================
#	This function writes Alarm 0-1 registers
#	Alarm0_1 => "1" Alarm 1; "0" Alarm 0
#	SetHourType => "1" 12-Hour Format; "0" 24-Hour Format
def WriteAlarmRegister(Alarm0_1, SetHourType):
	global _Alarm
	
	if (Alarm0_1 != 0):
		WriteSingleReg(RTCC_HW_ADD, ALM1SEC_ADD, _Alarm.Alm[1].Seconds.SecByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM1MIN_ADD, _Alarm.Alm[1].Minutes.MinByte.Byte0)
		if (SetHourType != 0):
			WriteSingleReg(RTCC_HW_ADD, ALM1HOUR_ADD, _Alarm.Alm[1].Hours12.Hour_12Byte.Byte0)
		else:
			WriteSingleReg(RTCC_HW_ADD, ALM1HOUR_ADD, _Alarm.Alm[1].Hours24.Hour_24Byte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM1WKDAY_ADD, _Alarm.Alm[1].WeekDay.WkDayByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM1DATE_ADD,  _Alarm.Alm[1].Date.DateByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM1MTH_ADD,   _Alarm.Alm[1].Month.MonthByte.Byte0)
	else:
		WriteSingleReg(RTCC_HW_ADD, ALM0SEC_ADD, _Alarm.Alm[0].Seconds.SecByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM0MIN_ADD, _Alarm.Alm[0].Minutes.MinByte.Byte0)
		if (SetHourType != 0):
			WriteSingleReg(RTCC_HW_ADD, ALM0HOUR_ADD, _Alarm.Alm[0].Hours12.Hour_12Byte.Byte0)
		else:
			WriteSingleReg(RTCC_HW_ADD, ALM0HOUR_ADD, _Alarm.Alm[0].Hours24.Hour_24Byte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM0WKDAY_ADD, _Alarm.Alm[0].WeekDay.WkDayByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM0DATE_ADD,  _Alarm.Alm[0].Date.DateByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, ALM0MTH_ADD,   _Alarm.Alm[0].Month.MonthByte.Byte0)
#===================================================================

#===================================================================
#	This function reads alarm 0-1 registers
#	Alarm0_1 => "1" Alarm 1; "0" Alarm 0
def ReadAlarmRegister(Alarm0_1):
	global _Alarm
		
	if (Alarm0_1 != 0):
		_Alarm.Alm[1].Seconds.SecByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, ALM1SEC_ADD)
		_Alarm.Alm[1].Minutes.MinByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, ALM1MIN_ADD)
		_Alarm.Alm[1].Hours12.Hour_12Byte.Byte0 = ReadSingleReg(RTCC_HW_ADD, ALM1HOUR_ADD)
		_Alarm.Alm[1].Hours24.Hour_24Byte.Byte0 = _Alarm.Alm[1].Hours12.Hour_12Byte.Byte0
		_Alarm.Alm[1].WeekDay.WkDayByte.Byte0   = ReadSingleReg(RTCC_HW_ADD, ALM1WKDAY_ADD)
		_Alarm.Alm[1].Date.DateByte.Byte0       = ReadSingleReg(RTCC_HW_ADD, ALM1DATE_ADD)
		_Alarm.Alm[1].Month.MonthByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, ALM1MTH_ADD)
	else:
		_Alarm.Alm[0].Seconds.SecByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, ALM0SEC_ADD)
		_Alarm.Alm[0].Minutes.MinByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, ALM0MIN_ADD)
		_Alarm.Alm[0].Hours12.Hour_12Byte.Byte0 = ReadSingleReg(RTCC_HW_ADD, ALM0HOUR_ADD)
		_Alarm.Alm[0].Hours24.Hour_24Byte.Byte0 = _Alarm.Alm[0].Hours12.Hour_12Byte.Byte0
		_Alarm.Alm[0].WeekDay.WkDayByte.Byte0   = ReadSingleReg(RTCC_HW_ADD, ALM0WKDAY_ADD)
		_Alarm.Alm[0].Date.DateByte.Byte0       = ReadSingleReg(RTCC_HW_ADD, ALM0DATE_ADD)
		_Alarm.Alm[0].Month.MonthByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, ALM0MTH_ADD)
#===================================================================



#===================================================================
#	This function writes PowerDown-Up registers
#	PowerDownUp => "1" PowerDown; "0" PowerUp
#	SetHourType => "1" 12-Hour Format; "0" 24-Hour Format
def WritePowerDownUpRegister(PowerDownUp, SetHourType):
	global _PwrTimeStamp
	
	if (PowerDownUp != 0):
		WriteSingleReg(RTCC_HW_ADD, PWRDWMIN_ADD, _PwrTimeStamp.Pwr[1].Minutes.MinByte.Byte0)
		if (SetHourType != 0):
			WriteSingleReg(RTCC_HW_ADD, PWRDWHOUR_ADD, _PwrTimeStamp.Pwr[1].Hours12.Hour_12Byte.Byte0)
		else:
			WriteSingleReg(RTCC_HW_ADD, PWRDWHOUR_ADD, _PwrTimeStamp.Pwr[1].Hours24.Hour_24Byte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, PWRDWDATE_ADD, _PwrTimeStamp.Pwr[1].Date.DateByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, PWRDWMTH_ADD,  _PwrTimeStamp.Pwr[1].Month.MonthByte.Byte0)
	else:
		WriteSingleReg(RTCC_HW_ADD, PWRUPMIN_ADD, _PwrTimeStamp.Pwr[0].Minutes.MinByte.Byte0)
		if (SetHourType != 0):
			WriteSingleReg(RTCC_HW_ADD, PWRUPHOUR_ADD, _PwrTimeStamp.Pwr[0].Hours12.Hour_12Byte.Byte0)
		else:
			WriteSingleReg(RTCC_HW_ADD, PWRUPHOUR_ADD, _PwrTimeStamp.Pwr[0].Hours24.Hour_24Byte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, PWRUPDATE_ADD, _PwrTimeStamp.Pwr[0].Date.DateByte.Byte0)
		WriteSingleReg(RTCC_HW_ADD, PWRUPMTH_ADD,  _PwrTimeStamp.Pwr[0].Month.MonthByte.Byte0)
#===================================================================

#===================================================================
#	This function reads PowerDown-Up registers
#	PowerDownUp => "1" PowerDown; "0" PowerUp
def ReadPowerDownUpRegister(PowerDownUp):
	global _PwrTimeStamp
	
	if (PowerDownUp != 0):
		_PwrTimeStamp.Pwr[1].Minutes.MinByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, PWRDWMIN_ADD)
		_PwrTimeStamp.Pwr[1].Hours12.Hour_12Byte.Byte0 = ReadSingleReg(RTCC_HW_ADD, PWRDWHOUR_ADD)
		_PwrTimeStamp.Pwr[1].Hours24.Hour_24Byte.Byte0 = _PwrTimeStamp.Pwr[1].Hours12.Hour_12Byte.Byte0
		_PwrTimeStamp.Pwr[1].Date.DateByte.Byte0       = ReadSingleReg(RTCC_HW_ADD, PWRDWDATE_ADD)
		_PwrTimeStamp.Pwr[1].Month.MonthByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, PWRDWMTH_ADD)
	else:
		_PwrTimeStamp.Pwr[0].Minutes.MinByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, PWRUPMIN_ADD)
		_PwrTimeStamp.Pwr[0].Hours12.Hour_12Byte.Byte0 = ReadSingleReg(RTCC_HW_ADD, PWRUPHOUR_ADD)
		_PwrTimeStamp.Pwr[0].Hours24.Hour_24Byte.Byte0 = _PwrTimeStamp.Pwr[0].Hours12.Hour_12Byte.Byte0
		_PwrTimeStamp.Pwr[0].Date.DateByte.Byte0       = ReadSingleReg(RTCC_HW_ADD, PWRUPDATE_ADD)
		_PwrTimeStamp.Pwr[0].Month.MonthByte.Byte0     = ReadSingleReg(RTCC_HW_ADD, PWRUPMTH_ADD)
#===================================================================
#======================================================================================================================================


#======================================================================================================================================
#==============================
#	SRAM/EEPROM DEDICATED FUNCTIONS
#==============================

#===================================================================
#	This function is useful to protect the 128 Byte EEPROM space.
#	To protect EEPROM spcae is necessary write a correct value into 
#	the "Eeprom Block Protection control register"
#==============================
#	128 Byte of EEPROM 
#	Start Address -> 0x00
#	End   Address -> 0x7F
#	Control Byte  -> 0xAE (Shifted value is 0x57)
#==============================
def Set_EEPROM_WriteProtection(Section):
	if (Section == 0):
		#	No Write Protected
		TempReg = 0x00
	elif (Section == 1):
		#	Protect Upper 1/4 (0x60 to 0x7F)
		TempReg = 0x04
	elif (Section == 2):
		#	Protect Upper 1/2 (0x40 to 0x7F)
		TempReg = 0x08		
	elif (Section == 3):
		#	Protect all
		TempReg = 0x0C
	else:
		TempReg = 0x00
		
	WriteSingleReg(EEPROM_HW_ADD, EEPROM_BLOCK_PROTECTION_ADD, TempReg)
#===================================================================

#===================================================================
#	This function is useful to write a byte into a protected EEPROM space.
#==============================
#	8 Byte of protected EEPROM 
#	Start Address -> 0xF0
#	End   Address -> 0xF7
#	Control Byte  -> 0xAE (Shifted value is 0x57)
#==============================
def WriteProtected_EEPROM(RegAdd, RegData):
	WriteSingleReg(RTCC_HW_ADD, EEUNLOCK_ADD, 0x55)
	WriteSingleReg(RTCC_HW_ADD, EEUNLOCK_ADD, 0xAA)
	WriteSingleReg(EEPROM_HW_ADD, RegAdd, RegData)
	#WriteSingleReg(EEPROM_HW_ADD, ((RegAdd & 0x07) | 0xF0), RegData)
#===================================================================
#======================================================================================================================================
