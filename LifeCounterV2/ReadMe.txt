##############
### ReadMe ###
##############


Introduction
############

This application was developped in order to test if the life counter of a Control Unit was still changing, in order to know if the Control unit has crashed.
The Control Unit configuration has to be defined in the LifeCounterConfig.ini.


INI file configuration
######################

There are 4 parameters to be configured in the INI file:
	- CU_NAME: 				This field is only used for display purposes in the alarm file
	- IP: 					IP v4 of the CU to be defined. This parameter needs to be correct in order to connect to the right CU
	- TEST_PERIOD: 			The application will test the value of the life counter at this period in seconds. 
							If '2' is defined, the application will check if the new counter value is different from the one that was available 2 seconds ago.
							Pay attention, for the XCU, the life counter is coded on a double byte and the counter is incremented each 100ms. 
							In order to be sure to avoid to get the same value,	the TEST_PERIOD should be lower than 65535*0.1=6553.
	- REGSITER_ADDRESS: 	Register address where the life counter can be read. For the XCU, it is 8192.
	- PROCESS_CHECK_TIME:	The application will display in the log file if the application is still running or not. This test is performed at this period.

Example
-------
[DEFAULT]
# To display in error logs
CU_NAME = XCU
# IPV4 (XXX.XXX.XXX.XXX)
IP = 10.130.13.20
# In seconds (float or integer)
TEST_PERIOD = 2
# (integer)
REGISTER_ADDRESS = 8192
# In seconds, higher or equal to TEST_PERIOD (integer)
PROCESS_CHECK_TIME = 1


Logs files
##########

A 'Logs' folder will be created in the parent folder of the application.
A new file will be automatically created everyday with the date of the day in its name.
A new line will be added each time the process is running and the PROCESS_CHECK_TIME is reached.
A new line will be added to the file of the day each time 
	- The process is running and the PROCESS_CHECK_TIME is reached ([INFO] tag);
	- There is a connection error with the CU ([ALARM] tag);
	- The new life counter value is equal to the previous one ([ALARM] tag).
	

Run the application
###################

Before starting the application, check that the INI file is well configured.

Windows
-------
In order to run the application, double click on LifeCounterCheck.exe.

Linux
-----
In order to run the application, open a terminal and go to the LifeCounterV2 directory.
Execute: ./LifeCounterCheck
In case of Graphic interface available, do not double click on the executable file, always use a terminal in order to have a display.
