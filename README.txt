Configuration management
------------------------
- Config file: LifeCounterConfig.ini

- The config file has to be filled following your site configuration. Each field is mandatory. 

- Fields
	- CU_NAME: Fill with the name you want to give to the CU. Only used for display.
	- IP: CU IP (v4) address.
	- TEST_PERIOD: In seconds (integer or float accepted). Should be lower than 30s and higher than 1s, depending on the CU.
	- REGISTER_ADDRESS: Depends on the Modbus interface (see CU ICD ==> Life counter).
						XCU: 8192
						FOVCU: 8212
						DNSHCU: 8212
	- PROCESS_CHECK_TIME: In seconds (integer). Must be higher than TEST_PERIOD. Period at a process running notification is written in the log.

- Pattern (example with XCU):
	[CU1]
	CU_NAME = XCU
	# IPV4 (XXX.XXX.XXX.XXX)
	IP = 10.130.13.20
	# In seconds (float or real)
	TEST_PERIOD = 10
	# (integer)
	REGISTER_ADDRESS = 8192
	# In seconds, higher or equal to TEST_PERIOD (integer)
	PROCESS_CHECK_TIME = 30

	
Bitmaps
-------
- Folder containing the bitmaps required by the application.

- The folder must be at the same level as the executable file.

- Must contain the following files:
	- state_healthy.png
	- state_unhealthy.png
	- state_unknown.png
	

Logs
----
- A log file is generated per CU and per day

- Log files contain ERROR, WARNING and INFO level.
