#==================================================================================
# ctypes type		C type						Python type
#==================================================================================
#   c_bool			_Bool						bool (1)
#----------------------------------------------------------------------------------
#   c_char			char						1-character string
#----------------------------------------------------------------------------------
#   c_wchar			wchar_t						1-character unicode string
#----------------------------------------------------------------------------------
#   c_byte			char						int/long
#----------------------------------------------------------------------------------
#   c_ubyte			unsigned char				int/long
#----------------------------------------------------------------------------------
#   c_short			short						int/long
#----------------------------------------------------------------------------------
#   c_ushort		unsigned short				int/long
#----------------------------------------------------------------------------------
#   c_int			int							int/long
#----------------------------------------------------------------------------------
#   c_uint			unsigned int				int/long
#----------------------------------------------------------------------------------
#   c_long			long						int/long
#----------------------------------------------------------------------------------
#   c_ulong			unsigned long				int/long
#----------------------------------------------------------------------------------
#   c_longlong		__int64 or long long		int/long
#----------------------------------------------------------------------------------
#   c_ulonglong		unsigned __int64 or 
#                   unsigned long long			int/long
#----------------------------------------------------------------------------------
#   c_float			float						float
#----------------------------------------------------------------------------------
#   c_double		double						float
#----------------------------------------------------------------------------------
#   c_longdouble	long double					float
#----------------------------------------------------------------------------------
#   c_char_p		char * (NUL terminated)		string or None
#----------------------------------------------------------------------------------
#   c_wchar_p		wchar_t * (NUL terminated)	unicode or None
#----------------------------------------------------------------------------------
#   c_void_p		void *	int/long or None	int/long or None
#==================================================================================

from ctypes import *

RTCC_HW_ADD	  =	0x6F	#	This address is got shifting the address 0xDE by one position on the right
EEPROM_HW_ADD =	0x57	#	This address is got shifting the address 0xAE by one position on the right

#===================================================================
#	MCP79410 RTCC Register Address
RTCSEC_ADD    =	0x00	#	Address TimeKeeping Seconds value register
RTCMIN_ADD    =	0x01	#	Address TimeKeeping Minutes value register
RTCHOUR_ADD	  =	0x02	#	Address TimeKeeping Hours value register
RTCWKDAY_ADD  =	0x03	#	Address TimeKeeping WeekDay value register
RTCDATE_ADD	  =	0x04	#	Address TimeKeeping Date value register
RTCMTH_ADD 	  =	0x05	#	Address TimeKeeping Month value register
RTCYEAR_ADD	  =	0x06	#	Address TimeKeeping Year value register
CONTROL_ADD	  =	0x07	#	Address RTCC control register
OSCTRIM_ADD	  =	0x08	#	Address Oscillator digital trim register
EEUNLOCK_ADD  =	0x09	#	Address Not a physical register
ALM0SEC_ADD	  =	0x0A	#	Address Alarm 0 Seconds value register
ALM0MIN_ADD	  =	0x0B	#	Address Alarm 0 Minutes value register
ALM0HOUR_ADD  =	0x0C	#	Address Alarm 0 Hours value register
ALM0WKDAY_ADD =	0x0D	#	Address Alarm 0 WeekDay value register
ALM0DATE_ADD  =	0x0E	#	Address Alarm 0 Date value register
ALM0MTH_ADD	  =	0x0F	#	Address Alarm 0 Month value register
RESERVED1_ADD =	0x10	#	Address Reserved
ALM1SEC_ADD	  = 0x11	#	Address Alarm 1 Seconds value register
ALM1MIN_ADD	  =	0x12	#	Address Alarm 1 Minutes value register
ALM1HOUR_ADD  =	0x13	#	Address Alarm 1 Hours value register
ALM1WKDAY_ADD =	0x14	#	Address Alarm 1 WeekDay value register
ALM1DATE_ADD  =	0x15	#	Address Alarm 1 Date value register
ALM1MTH_ADD	  =	0x16	#	Address Alarm 1 Month value register
RESERVED2_ADD =	0x17	#	Address Reserved
PWRDWMIN_ADD  =	0x18	#	Address Power-Down TimeStamp Minutes value register
PWRDWHOUR_ADD =	0x19	#	Address Power-Down TimeStamp Hours value register
PWRDWDATE_ADD =	0x1A	#	Address Power-Down TimeStamp Date value register
PWRDWMTH_ADD  =	0x1B	#	Address Power-Down TimeStamp Month value register
PWRUPMIN_ADD  =	0x1C	#	Address Power-Up TimeStamp Minutes value register
PWRUPHOUR_ADD =	0x1D	#	Address Power-Up TimeStamp Hours value register
PWRUPDATE_ADD =	0x1E	#	Address Power-Up TimeStamp Date value register
PWRUPMTH_ADD  =	0x1F	#	Address Power-Up TimeStamp Month value register
#===================================================================

#===================================================================
#	Control Bits const. Examples of use
OSCILLATOR_BIT_ON	   = 0x80	#	Start Oscillator Bit (RTCSEC   | OSCILLATOR_BIT_ON)
OSCILLATOR_BIT_OFF	   = 0x7F 	#	Stop  Oscillator Bit (RTCSEC   & OSCILLATOR_BIT_OFF)
_12_HOUR_ON			   = 0x40 	#	12 Hour Format       (RTCHOUR  | _12_HOUR_ON)
_24_HOUR_ON			   = 0xBF	#	24 Hour Format       (RTCHOUR  & _24_HOUR_ON)
VBAT_ON				   = 0x08	#	Enable Vbat input    (RTCWKDAY | VBAT_ON) 
VBAT_OFF			   = 0xBF	#	Disable Vbat input   (RTCWKDAY & VBAT_OFF) 

OUT_LOGIC_LEVEL_HIGH   = 0x80	#	MFP signal level is logic HIGH        (CONTROL | OUT_LOGIC_LEVEL_HIGH)
OUT_LOGIC_LEVEL_LOW    = 0x7F	#	MFP signal level is logic LOW         (CONTROL | OUT_LOGIC_LEVEL_LOW)
SQUARE_WAVE_OUTPUT_ON  = 0x40	#	Enable Square Wave Clock Output Mode  (CONTROL | SQUARE_WAVE_OUTPUT_ON)
SQUARE_WAVE_OUTPUT_OFF = 0xBF	#	Disable Square Wave Clock Output Mode (CONTROL & SQUARE_WAVE_OUTPUT_OFF)
ALARM1_ON			   = 0x20	#	Alarm 1 Enabled                       (CONTROL | ALARM1_ON)
ALARM1_OFF			   = 0xDF	#	Alarm 1 Disabled                      (CONTROL | ALARM1_OFF)
ALARM0_ON			   = 0x10	#	Alarm 0 Enabled                       (CONTROL | ALARM0_ON)
ALARM0_OFF			   = 0xEF	#	Alarm 0 Disabled                      (CONTROL | ALARM0_OFF)
X1_EXTOSC_ON	 	   = 0x08	#	Enable X1 pin         				  (CONTROL | X1_EXTOSC_ON)
X1_EXTOSC_OFF		   = 0xF7	#	Disable X1 pin         				  (CONTROL | X1_EXTOSC_OFF)
CRSTRIM_ON			   = 0x04	#	Enable Coarse Trim mode (if SQWEN=1)  (CONTROL | CRSTRIM_ON)
CRSTRIM_OFF			   = 0xFB	#	Disable Coarse Trim mode         	  (CONTROL | CRSTRIM_OFF)
SQWFS_1Hz			   = 0xFC	#	If SQWEN=1 and CSTRIM=0 F=1Hz         (CONTROL & SQWFS_1Hz)
SQWFS_4096Hz		   = 0x01	#	If SQWEN=1 and CSTRIM=0 F=4096Hz     ((CONTROL & SQWFS_1Hz) | SQWFS_4096Hz)
SQWFS_8192Hz		   = 0x02	#	If SQWEN=1 and CSTRIM=0 F=8192Hz     ((CONTROL & SQWFS_1Hz) | SQWFS_8192Hz)
SQWFS_32768Hz		   = 0x03	#	If SQWEN=1 and CSTRIM=0 F=32768Hz    ((CONTROL & SQWFS_1Hz) | SQWFS_32768Hz)

TEST_POWER_FAIL		   = 0x10	#	TEST POWER FAIL STATUS (RTCWKDAY & TEST_POWER_FAIL) 
TEST_OSCRUN			   = 0x20	#	TEST OSCRUN STATUS     (RTCWKDAY & TEST_OSCRUN) 
TEST_LEAPYEAR		   = 0x20	#	TEST LEAPYEAR STATUS   (RTCMTH   & TEST_OSCRUN) 
#===================================================================

#===================================================================
#	TimeKeeper data registers (CONSTANT Example)
RTCSEC_REG	 = 0x80	#	TimeKeeping Seconds value register
					#	Bxxxxxxxx
					#	 ||||||||
					#	 ||||++++--->	SECONE -> Bynary-Coded Decimal Value of Second's Ones Digit (0-9)
					#	 |+++------->	SECTEN -> Bynary-Coded Decimal Value of Second's Tens Digit (0-5)
					#	 +---------->	ST     -> Start oscillator bit (1->Enabled; 0->Disabled)
RTCMIN_REG   = 0x00	#	TimeKeeping Minutes value register
					#	Bxxxxxxxx
					#	 ||||||||
					#	 ||||++++--->	MINONE -> Bynary-Coded Decimal Value of Minute's Ones Digit (0-9)
					#	 |+++------->	MINTEN -> Bynary-Coded Decimal Value of Minute's Tens Digit (0-5)
					#	 +---------->	Unimplemented
RTCHOUR_REG	 = 0x00	#	TimeKeeping Hours value register
					#	Bxxxxxxxx	(12-Hour Format)
					#	 ||||||||
					#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
					#	 |||+------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-1)
					#	 ||+-------->	~AM/PM -> AM/PM Indicator bit (1->PM; 0->AM)
					#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
					#	 +---------->	Unimplemented
					#	Bxxxxxxxx	(24-Hour Format)
					#	 ||||||||
					#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
					#	 ||++------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-2)
					#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
					#	 +---------->	Unimplemented										
RTCWKDAY_REG = 0x08	#	TimeKeeping WeekDay value register										
					#	Bxxxxxxxx
					#	 ||||||||
					#	 |||||+++--->	WKDAY   -> Bynary-Coded Decimal Value of Day of Week Digit (1-7)
					#	 ||||+------>	VBATEN  -> Externally Battery Backup Supply Enable Bit (1->Vbat input is Enabled;
					#	 ||||																	0->Vbat input is Disabled)
					#	 |||+------->	PWRFAIL -> Power Failure Status Bit (1->Primary power was lost and the power-fail
					#	 |||													time-stamp registers have been loaded (Must be cleared
					#	 |||													in software). Clearing this bit resets the power-fail
					#	 |||													time-stamp register to 0);
					#	 ||| 												 0-> Primary power has not been lost
					#	 ||+--------->	OSCRUN  -> Oscillator status bit (Read Only) (1-> Oscillator is enabled and running;
					#	 ||															  0-> Oscillator has stopped or has been disabled)										
					#	 ++---------->	Unimplemented
RTCDATE_REG	 = 0x00	#	TimeKeeping Date value register
					#	Bxxxxxxxx
					#	 ||||||||
					#	 ||||++++--->	DATEONE -> Bynary-Coded Decimal Value of Date's Ones Digit (0-9)
					#	 ||++------->	DATETEN -> Bynary-Coded Decimal Value of Date's Tens Digit (0-3)
					#	 ++--------->	Unimplemented
RTCMTH_REG	 = 0x00	#	TimeKeeping Month value register
					#	Bxxxxxxxx
					#	 ||||||||
					#	 ||||++++--->	MTHONE -> Bynary-Coded Decimal Value of Months's Ones Digit (0-9)
					#	 |||+------->	MTHTEN -> Bynary-Coded Decimal Value of Month's Tens Digit (0-1)
					#	 ||+-------->	LPYR   -> Leap Year Bit (1->Year is leap year; 0->Year is not a leap year)
					#	 ++--------->	Unimplemented
RTCYEAR_REG	 = 0x00	#	TimeKeeping Year value register
					#	Bxxxxxxxx
					#	 ||||||||
					#	 ||||++++--->	YRONE -> Bynary-Coded Decimal Value of Year's Ones Digit (0-9)
					#	 ++++------->	YRTEN -> Bynary-Coded Decimal Value of Year's Tens Digit (0-9)
#===================================================================

#===================================================================
CONTROL_REG	= 0x00	#	RTCC control register
					#	Bxxxxxxxx
					#	 ||||||||
					#	 ||||||++--->	SQWFS   -> Square Wave Clock Output Frequency:
					#	 ||||||                    if SQWEN=1 And CRSTRIM=0:
					#	 ||||||					      00 -> 1 Hz
					#	 ||||||						  01 -> 4096 Hz
					#	 ||||||						  10 -> 8192 Hz
					#	 ||||||						  11 -> 32768 Hz
					#	 ||||||                    if SQWEN=0 And CRSTRIM=1 (Unused)
					#	 |||||+----->	CRSTRIM -> Coarse Trim Mode Enable bit (1->Enabled Coarse Trim mode; 0->Disabled Coarse Trim mode)
					#	 ||||+------>	EXTOSC  -> External Oscillator Input bit (1->Enable X1 pin to be driven by external 32768 Hz source;
					#	 ||||													  0->Disable esternal 32768 Hz input)
					#    |||+------->   ALM0EN  -> Alarm 0 Modeule Enable bit (1->Alarm 0 Enabled; 0->Alarm 0 Disabled)
					#    ||+-------->   ALM1EN  -> Alarm 1 Modeule Enable bit (1->Alarm 1 Enabled; 0->Alarm 1 Disabled)
					#    |+--------->   SQWEN   -> Square Wave Output Enable Bit (1->Enable Square Wave Clock Output mode;
					#    |                                                        0->Disable Square Wave Clock Output mode)
					#    +---------->   OUT		-> Logic Level for General Purpose Output bit (SQWEN=0; ALM0EN=0; ALM1EN=0)
					#					   			1->MFP Signal level is logic High
					#							   	0->MFP Signal level is logic Low
#===================================================================

#===================================================================
#	Alarm 0 data registers (CONSTANT)
ALM0SEC_REG   = 0x00	#	Alarm 0 Seconds value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	SECONE -> Bynary-Coded Decimal Value of Second's Ones Digit (0-9)
						#	 |+++------->	SECTEN -> Bynary-Coded Decimal Value of Second's Tens Digit (0-5)
						#	 +---------->	Unimplemented
ALM0MIN_REG   = 0x00	#	Alarm 0 Minutes value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MINONE -> Bynary-Coded Decimal Value of Minute's Ones Digit (0-9)
						#	 |+++------->	MINTEN -> Bynary-Coded Decimal Value of Minute's Tens Digit (0-5)
						#	 +---------->	Unimplemented
ALM0HOUR_REG  =	0x00	#	Alarm 0 Hours value register
						#	Bxxxxxxxx	(12-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 |||+------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-1)
						#	 ||+-------->	~AM/PM -> AM/PM Indicator bit (1->PM; 0->AM)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
						#	Bxxxxxxxx	(24-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 ||++------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-2)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
ALM0WKDAY_REG = 0x00	#	Alarm 0 WeekDay value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 |||||+++--->	WKDAY   -> Bynary-Coded Decimal Value of Day bits (1-7)
						#	 ||||+------>	ALM0IF  -> Alarm interrupt Flag bit (1->Alarm match occurred (Must be cleared in software);
						#	 |||| 											 	 0->Alarm match did not occur)
						#	 |+++------->	ALM0MSK -> Alarm Mask bits 000->Seconds match
						#    |                                         001->Minutes match
						#    |										   010->Hours match
						#    |										   011->Day of week match
						#    |										   100->Date match
						#    |										   101->Reserved
						#    |										   110->Reserved
						#    |										   111->Seconds, Minutes, Hour, Day of Week, Date and Month match
						#	 +---------->	ALMPOL  -> Alarm Interrupt Output Polarity bit (1->Asserted output state of MFP is a logic high level;
						#																	0->Asserted output state of MFP is a logic low level)
ALM0DATE_REG  = 0x00	#	Alarm 0 Date value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	DATEONE -> Bynary-Coded Decimal Value of Date's Ones Digit (0-9)
						#	 ||++------->	DATETEN -> Bynary-Coded Decimal Value of Date's Tens Digit (0-3)
						#	 ++--------->	Unimplemented
ALM0MTH_REG   = 0x00	#	Alarm 0 Month value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MTHONE -> Bynary-Coded Decimal Value of Months's Ones Digit (0-9)
						#	 |||+------->	MTHTEN -> Bynary-Coded Decimal Value of Month's Tens Digit (0-1)
						#	 ||+-------->	LPYR   -> Leap Year Bit (1->Year is leap year; 0->Year is not a leap year)
						#	 ++--------->	Unimplemented																		
#===================================================================

#===================================================================
#	Alarm 1 data registers (CONSTANT)
ALM1SEC_REG	  = 0x00	#	Alarm 1 Seconds value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	SECONE -> Bynary-Coded Decimal Value of Second's Ones Digit (0-9)
						#	 |+++------->	SECTEN -> Bynary-Coded Decimal Value of Second's Tens Digit (0-5)
						#	 +---------->	Unimplemented
ALM1MIN_REG	  = 0x00	#	Alarm 1 Minutes value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MINONE -> Bynary-Coded Decimal Value of Minute's Ones Digit (0-9)
						#	 |+++------->	MINTEN -> Bynary-Coded Decimal Value of Minute's Tens Digit (0-5)
						#	 +---------->	Unimplemented
ALM1HOUR_REG  = 0x00	#	Alarm 1 Hours value register
						#	Bxxxxxxxx	(12-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 |||+------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-1)
						#	 ||+-------->	~AM/PM -> AM/PM Indicator bit (1->PM; 0->AM)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
						#	Bxxxxxxxx	(24-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 ||++------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-2)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
ALM1WKDAY_REG =	0x00	#	Alarm 1 WeekDay value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 |||||+++--->	WKDAY   -> Bynary-Coded Decimal Value of Day bits (1-7)
						#	 ||||+------>	ALM0IF  -> Alarm interrupt Flag bit (1->Alarm match occurred (Must be cleared in software);
						#	 |||| 												0->Alarm match did not occur)
						#	 |+++------->	ALM0MSK -> Alarm Mask bits 000->Seconds match
						#    |                                         001->Minutes match
						#    |										   010->Hours match
						#    |										   011->Day of week match
						#    |										   100->Date match
						#    |										   101->Reserved
						#    |										   110->Reserved
						#    |										   111->Seconds, Minutes, Hour, Day of Week, Date and Month match
						#	 +---------->	ALMPOL  -> Alarm Interrupt Output Polarity bit (1->Asserted output state of MFP is a logic high level;
						#																	0->Asserted output state of MFP is a logic low level)
ALM1DATE_REG  = 0x00	#	Alarm 1 Date value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	DATEONE -> Bynary-Coded Decimal Value of Date's Ones Digit (0-9)
						#	 ||++------->	DATETEN -> Bynary-Coded Decimal Value of Date's Tens Digit (0-3)
						#	 ++--------->	Unimplemented
ALM1MTH_REG	  = 0x00	#	Alarm 1 Month value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MTHONE -> Bynary-Coded Decimal Value of Months's Ones Digit (0-9)
						#	 |||+------->	MTHTEN -> Bynary-Coded Decimal Value of Month's Tens Digit (0-1)
						#	 ||+-------->	LPYR   -> Leap Year Bit (1->Year is leap year; 0->Year is not a leap year)
						#	 ++--------->	Unimplemented																		
#===================================================================

#===================================================================
#	PowerDown Time-Stamp data registers (CONSTANT)
PWRDWMIN_REG  =	0x00	#	Power-Down TimeStamp Minutes value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MINONE -> Bynary-Coded Decimal Value of Minute's Ones Digit (0-9)
						#	 |+++------->	MINTEN -> Bynary-Coded Decimal Value of Minute's Tens Digit (0-5)
						#	 +---------->	Unimplemented
PWRDWHOUR_REG =	0x00	#	Power-Down TimeStamp Hours value register
						#	Bxxxxxxxx	(12-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 |||+------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-1)
						#	 ||+-------->	~AM/PM -> AM/PM Indicator bit (1->PM; 0->AM)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
						#	Bxxxxxxxx	(24-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 ||++------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-2)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
PWRDWDATE_REG =	0x00	#	Power-Down TimeStamp Date value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	DATEONE -> Bynary-Coded Decimal Value of Date's Ones Digit (0-9)
						#	 ||++------->	DATETEN -> Bynary-Coded Decimal Value of Date's Tens Digit (0-3)
						#	 ++--------->	Unimplemented
PWRDWMTH_REG  = 0x00	#	Power-Down TimeStamp Month value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MTHONE -> Bynary-Coded Decimal Value of Months's Ones Digit (0-9)
						#	 |||+------->	MTHTEN -> Bynary-Coded Decimal Value of Month's Tens Digit (0-1)
						#	 +++-------->	WKDAY  -> Bynary-Coded Decimal Value of Day bits (1-7)
#===================================================================

#===================================================================
#	PowerUp Time-Stamp data registers (CONSTANT)										
PWRUPMIN_REG  =	0x00	#	Power-Down TimeStamp Minutes value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MINONE -> Bynary-Coded Decimal Value of Minute's Ones Digit (0-9)
						#	 |+++------->	MINTEN -> Bynary-Coded Decimal Value of Minute's Tens Digit (0-5)
						#	 +---------->	Unimplemented
PWRUPHOUR_REG =	0x00	#	Power-Down TimeStamp Hours value register
						#	Bxxxxxxxx	(12-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 |||+------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-1)
						#	 ||+-------->	~AM/PM -> AM/PM Indicator bit (1->PM; 0->AM)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
						#	Bxxxxxxxx	(24-Hour Format)
						#	 ||||||||
						#	 ||||++++--->	HRONE  -> Bynary-Coded Decimal Value of Hour's Ones Digit (0-9)
						#	 ||++------->	HRTEN  -> Bynary-Coded Decimal Value of Hour's Tens Digit (0-2)
						#	 |+--------->	12/~24 -> 12 or 24 Hour Time Format bit (1->12 Hour Format; 0->24 Hour Format)										
						#	 +---------->	Unimplemented
PWRUPDATE_REG =	0x00	#	Power-Down TimeStamp Date value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	DATEONE -> Bynary-Coded Decimal Value of Date's Ones Digit (0-9)
						#	 ||++------->	DATETEN -> Bynary-Coded Decimal Value of Date's Tens Digit (0-3)
						#	 ++--------->	Unimplemented
PWRUPMTH_REG  = 0x00	#	Power-Down TimeStamp Month value register
						#	Bxxxxxxxx
						#	 ||||||||
						#	 ||||++++--->	MTHONE -> Bynary-Coded Decimal Value of Months's Ones Digit (0-9)
						#	 |||+------->	MTHTEN -> Bynary-Coded Decimal Value of Month's Tens Digit (0-1)
						#	 +++-------->	WKDAY  -> Bynary-Coded Decimal Value of Day bits (1-7)
#===================================================================
	
#===================================================================										
#	MCP79410 EEPROM Register Address

EEPROM_START_ADD			= 0x00
EEPROM_STOP_ADD				= 0x7F
EEPROM_BLOCK_PROTECTION_ADD = 0xFF

PROTECTED_EEPROM_START_ADD	= 0xF0
PROTECTED_EEPROM_STOP_ADD	= 0xF7
#===================================================================

DataArray = c_ubyte * 16

#======================================================================================================================================
#===================================================================
class CtrlBit(Structure):
	_fields_ = [("SquareWaveFreqOutput",   c_uint8, 2),	            
			    ("CoarseTrimEnable",       c_uint8, 1),
		   	    ("ExtOscInput",            c_uint8, 1),
		   	    ("Alarm0_Enable",          c_uint8, 1),
		   	    ("Alarm1_Enable",          c_uint8, 1),
		   	    ("SquareWaveOutputEnable", c_uint8, 1),
		   	    ("LogicLevelOutput",       c_uint8, 1)]
		   	    
class CtrlByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class CtrlReg(Union):
	_fields_ = [("ControlBit",  CtrlBit),
				("ControlByte", CtrlByte)]					   	
#===================================================================

#===================================================================
class TrimBit(Structure):
	_fields_ = [("TrimSignBit", c_uint8, 1),	            
			    ("TrimValue",   c_uint8, 7)]

class TrimByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class OSC_TrimReg(Union):
	_fields_ = [("OscTrimBit",  TrimBit),
				("OscTrimByte", TrimByte)]	   	    	
#===================================================================
#======================================================================================================================================

#======================================================================================================================================
#	TimeKeeper data registers
class TmkSecBit(Structure):
	_fields_ = [("SecOne",   c_uint8, 4),	            
			    ("SecTen",   c_uint8, 3),
		   	    ("StartOsc", c_uint8, 1)]

class TmkSecByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperSeconds(Union):
	_fields_ = [("SecBit",  TmkSecBit),
				("SecByte", TmkSecByte)]            

#---------------------------------------------------------

class TmkMinBit(Structure):
	_fields_ = [("MinOne", c_uint8, 4),	            
			    ("MinTen", c_uint8, 3),
		   	    ("Free",   c_uint8, 1)]

class TmkMinByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperMinutes(Union):
	_fields_ = [("MinBit",  TmkMinBit),
				("MinByte", TmkMinByte)]            

#---------------------------------------------------------

class TmkHour_12Bit(Structure):
	_fields_ = [("HrOne",  c_uint8, 4),	            
			    ("HrTen",  c_uint8, 1),
			    ("AmPm",   c_uint8, 1),
			    ("_12_24", c_uint8, 1),
		   	    ("Free",   c_uint8, 1)]

class TmkHour_12Byte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperHours12(Union):
	_fields_ = [("Hour_12Bit",  TmkHour_12Bit),
				("Hour_12Byte", TmkHour_12Byte)]            

#---------------------------------------------------------

class TmkHour_24Bit(Structure):
	_fields_ = [("HrOne",  c_uint8, 4),	            
			    ("HrTen",  c_uint8, 2),
			    ("_12_24", c_uint8, 1),
		   	    ("Free",   c_uint8, 1)]

class TmkHour_24Byte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperHours24(Union):
	_fields_ = [("Hour_24Bit",  TmkHour_24Bit),
				("Hour_24Byte", TmkHour_24Byte)]            

#---------------------------------------------------------

class TmkWkDayBit(Structure):
	_fields_ = [("WkDay",   c_uint8, 3),	            
			    ("VbatEn",  c_uint8, 1),
			    ("PwrFail", c_uint8, 1),
			    ("OSCrun",  c_uint8, 1),
		   	    ("Free",    c_uint8, 2)]

class TmkWkDayByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperWeekDay(Union):
	_fields_ = [("WkDayBit",  TmkWkDayBit),
				("WkDayByte", TmkWkDayByte)]            

#---------------------------------------------------------

class TmkDateBit(Structure):
	_fields_ = [("DateOne", c_uint8, 4),	            
			    ("DateTen", c_uint8, 2),
		   	    ("Free",    c_uint8, 2)]

class TmkDateByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperDate(Union):
	_fields_ = [("DateBit",  TmkDateBit),
				("DateByte", TmkDateByte)]            

#---------------------------------------------------------

class TmkMonthBit(Structure):
	_fields_ = [("MonthOne", c_uint8, 4),	            
			    ("MonthTen", c_uint8, 1),
			    ("LeapYear", c_uint8, 1),
		   	    ("Free",     c_uint8, 2)]

class TmkMonthByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperMonth(Union):
	_fields_ = [("MonthBit",  TmkMonthBit),
				("MonthByte", TmkMonthByte)]            

#---------------------------------------------------------

class TmkYearBit(Structure):
	_fields_ = [("YearOne", c_uint8, 4),	            
			    ("YearTen", c_uint8, 4)]

class TmkYearByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class TimeKeeperYear(Union):
	_fields_ = [("YearBit",  TmkYearBit),
				("YearByte", TmkYearByte)]            

#---------------------------------------------------------

class TimeKeeperStruct(Structure):
	_fields_ = [("Seconds",  TimeKeeperSeconds),
				("Minutes",  TimeKeeperMinutes),
				("Hours12",  TimeKeeperHours12),
				("Hours24",  TimeKeeperHours24),
				("WeekDay",  TimeKeeperWeekDay),
				("Date",     TimeKeeperDate),
				("Month",    TimeKeeperMonth),
				("Year",     TimeKeeperYear)]		
#======================================================================================================================================

#======================================================================================================================================
#	Alarm data registers
class AlmSecBit(Structure):
	_fields_ = [("SecOne", c_uint8, 4),	            
			    ("SecTen", c_uint8, 3),
		   	    ("Free",   c_uint8, 1)]

class AlmSecByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class AlarmSeconds(Union):
	_fields_ = [("SecBit",  AlmSecBit),
				("SecByte", AlmSecByte)]            

#---------------------------------------------------------

class AlmMinBit(Structure):
	_fields_ = [("MinOne", c_uint8, 4),	            
			    ("MinTen", c_uint8, 3),
		   	    ("Free",   c_uint8, 1)]

class AlmMinByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class AlarmMinutes(Union):
	_fields_ = [("MinBit",  AlmMinBit),
				("MinByte", AlmMinByte)]            

#---------------------------------------------------------

class AlmHour_12Bit(Structure):
	_fields_ = [("HrOne",  c_uint8, 4),	            
			    ("HrTen",  c_uint8, 1),
			    ("AmPm",   c_uint8, 1),
			    ("_12_24", c_uint8, 1),
		   	    ("Free",   c_uint8, 1)]

class AlmHour_12Byte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class AlarmHours12(Union):
	_fields_ = [("Hour_12Bit",  AlmHour_12Bit),
				("Hour_12Byte", AlmHour_12Byte)]            

#---------------------------------------------------------

class AlmHour_24Bit(Structure):
	_fields_ = [("HrOne",  c_uint8, 4),	            
			    ("HrTen",  c_uint8, 2),
			    ("_12_24", c_uint8, 1),
		   	    ("Free",   c_uint8, 1)]

class AlmHour_24Byte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class AlarmHours24(Union):
	_fields_ = [("Hour_24Bit",  AlmHour_24Bit),
				("Hour_24Byte", AlmHour_24Byte)]            

#---------------------------------------------------------

class AlmWkDayBit(Structure):
	_fields_ = [("WkDay",     c_uint8, 3),	            
			    ("AlarmIF",   c_uint8, 1),
			    ("AlarmMask", c_uint8, 3),
			    ("AlarmPol",  c_uint8, 1)]

class AlmWkDayByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class AlarmWeekDay(Union):
	_fields_ = [("WkDayBit",  AlmWkDayBit),
				("WkDayByte", AlmWkDayByte)]            

#---------------------------------------------------------

class AlmDateBit(Structure):
	_fields_ = [("DateOne", c_uint8, 4),	            
			    ("DateTen", c_uint8, 2),
		   	    ("Free",    c_uint8, 2)]

class AlmDateByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class AlarmDate(Union):
	_fields_ = [("DateBit",  AlmDateBit),
				("DateByte", AlmDateByte)]            

#---------------------------------------------------------

class AlmMonthBit(Structure):
	_fields_ = [("MonthOne", c_uint8, 4),	            
			    ("MonthTen", c_uint8, 1),
		   	    ("Free",     c_uint8, 3)]

class AlmMonthByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class AlarmMonth(Union):
	_fields_ = [("MonthBit",  AlmMonthBit),
				("MonthByte", AlmMonthByte)]            

#---------------------------------------------------------

class AlarmStruct(Structure):
	_fields_ = [("Seconds", AlarmSeconds),
				("Minutes", AlarmMinutes),
				("Hours12", AlarmHours12),
				("Hours24", AlarmHours24),
				("WeekDay", AlarmWeekDay),
				("Date",    AlarmDate),
				("Month",   AlarmMonth)] 

class AlarmArray(Structure):
	_fields_ = [("Alm",  AlarmStruct * 2)] 
#======================================================================================================================================


#======================================================================================================================================
#	PowerDown/PowerUp TimeStamp data registers
#	PowerTimeStamp[0] Stores PowerDown TimeStamp
#	PowerTimeStamp[1] Stores PowerUp TimeStamp
class PwrMinBit(Structure):
	_fields_ = [("MinOne", c_uint8, 4),	            
			    ("MinTen", c_uint8, 3),
		   	    ("Free",   c_uint8, 1)]

class PwrMinByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class PowerMinutes(Union):
	_fields_ = [("MinBit",  PwrMinBit),
				("MinByte", PwrMinByte)]           

#---------------------------------------------------------

class PwrHour_12Bit(Structure):
	_fields_ = [("HrOne",  c_uint8, 4),	            
			    ("HrTen",  c_uint8, 1),
			    ("AmPm",   c_uint8, 1),
			    ("_12_24", c_uint8, 1),
		   	    ("Free",   c_uint8, 1)]

class PwrHour_12Byte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class PowerHours12(Union):
	_fields_ = [("Hour_12Bit",  PwrHour_12Bit),
				("Hour_12Byte", PwrHour_12Byte)]            

#---------------------------------------------------------

class PwrHour_24Bit(Structure):
	_fields_ = [("HrOne",  c_uint8, 4),	            
			    ("HrTen",  c_uint8, 2),
			    ("_12_24", c_uint8, 1),
		   	    ("Free",   c_uint8, 1)]

class PwrHour_24Byte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class PowerHours24(Union):
	_fields_ = [("Hour_24Bit",  PwrHour_24Bit),
				("Hour_24Byte", PwrHour_24Byte)]            

#---------------------------------------------------------

class PwrDateBit(Structure):
	_fields_ = [("DateOne", c_uint8, 4),	            
			    ("DateTen", c_uint8, 2),
		   	    ("Free",    c_uint8, 2)]

class PwrDateByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class PowerDate(Union):
	_fields_ = [("DateBit",  PwrDateBit),
				("DateByte", PwrDateByte)]            

#---------------------------------------------------------

class PwrMonthBit(Structure):
	_fields_ = [("MonthOne", c_uint8, 4),	            
			    ("MonthTen", c_uint8, 1),
		   	    ("WkDay",    c_uint8, 3)]

class PwrMonthByte(Structure):	
	_fields_ = [("Byte0", c_uint8)]
	
class PowerMonth(Union):
	_fields_ = [("MonthBit",  PwrMonthBit),
				("MonthByte", PwrMonthByte)]            

#---------------------------------------------------------

class PowerStruct(Structure):
	_fields_ = [("Minutes", PowerMinutes),
				("Hours12", PowerHours12),
				("Hours24", PowerHours24),
				("Date",    PowerDate),
				("Month",   PowerMonth)] 

class PowerArray(Structure):
	_fields_ = [("Pwr",  PowerStruct * 2)] 
#======================================================================================================================================
