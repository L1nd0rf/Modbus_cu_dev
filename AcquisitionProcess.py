###########
# Imports #
###########

import time
import os
from pyModbusTCP.client import ModbusClient
from datetime import datetime
from threading import Timer
from tkinter.messagebox import *
import logging
from CuStatus import CuStatus

#############
# Constants #
#############

SERVER_PORT = 502
MODBUS_TIMEOUT = 5.0
MAX_CONNECTION_ATTEMPT = 3

####################
# Class definition #
####################


class AcquisitionProcess:
    """
    Class that handles the Modbus communication between the application and the target CUs.

    The class implements methods allowing:
    - Modbus communication establishment;
    - Reading register value from a Modbus server;
    - Comparing this value to the previous one to check if the CU is still alive.
    """

    def __init__(self, config, gui):
        """
        AcquisitionProcess class constructor.

        :param config: (CuConfig object) Contains an object that handles the CU config file (LifeCounterConfig.ini)
        :param gui: (GuiManagement object) Contains an object that handles the GUI display.
        """
        # Communication configuration
        self.config_cu_name = config.get("cu_name")
        self.config_server_host = config.get("server_host")
        self.config_test_period = config.get("test_period")
        self.config_register_address = config.get("register_address")
        self.config_process_check_time = config.get("process_check_time")

        # Modbus communication definition
        self.client = ModbusClient()
        self.client.host(self.config_server_host)
        self.client.port(SERVER_PORT)
        self.client.timeout(MODBUS_TIMEOUT)

        # Values initialization
        self.previous_counter_value = -1
        self.previous_process_check = 0
        self.previous_process_time = datetime.now()
        self.process_startup = True
        self.process_started = False
        self.connection_attempt = 0

        # Define new name for alarms tracking file, changes everyday
        self.day_file_name = "{}-{}_logs.txt".format(time.strftime("%Y_%m_%d"), self.config_cu_name)

        # Objects initialization
        self.thread = None
        self.logger = None

        # GUI textbox declaration
        self.gui = gui

    def __del__(self):
        """
        Method called at object deletion.

        Override in order to cancel thread and close communication socket in case they are running.

        :return: N/A
        """
        if self.client.is_open():
            self.client.close()

        if self.thread:
            self.thread.cancel()

    def __setupLogger(self, name, log_file, level=logging.INFO):
        """
        Private method that creates a logger for the
        :param name: (string) Logger name
        :param log_file: (string) File pâth to write logs
        :param level: (logging.level) Level of information to write
        :return: (logging) Logger dedicated to current CU instantiated
        """
        # Define logs format
        formatter = logging.Formatter(fmt='[%(levelname)s] - %(asctime)s - %(message)s',
                                      datefmt='%Y/%m/%d %I:%M:%S %p')

        if not os.path.exists('./Logs/'):
            os.makedirs('./Logs/')

        # Define file handler with path and format
        handler = logging.FileHandler("./Logs/" + log_file)
        handler.setFormatter(formatter)

        # Define logger with name, level and adding the file handler
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    def __handleFunction(self):
        """
        Private method that handles the thread of the the current CU communication.

        This method also defines the log files, the logger format and ensures that the prerequisites are met before
        starting the application.

        :return: N/A
        """
        try:
            # Notify if process still running
            self.__notifyRunning()

            # Open or reconnect TCP to server
            self.__modbusClientConnection()

            # Check that CU is still running
            self.__processCheck()

        except AttributeError as e:
            error_message = e + \
                            "\nThe process was stopped during communication establishment to" + \
                            self.config_cu_name
            self.__displayError(error_message)

        # Handle thread
        if self.process_started:
            self.thread = Timer(self.config_test_period, self.__handleFunction)
            self.thread.start()

    def start(self):
        """
        Public method that starts the data acquisition through a Modbus/TCP communication.

        :return: N/A
        """
        if not self.process_started:
            self.connection_attempt = 0
            display_message = "================================\n" + \
                              self.config_cu_name + " Life counter process started\n" \
                              "================================"
            self.__displayLog(display_message)
            self.logger = self.__setupLogger(self.config_cu_name, self.day_file_name)
            self.thread = Timer(self.config_test_period, self.__handleFunction)
            self.thread.start()
            self.process_started = True
        else:
            showinfo(self.config_cu_name + " info", self.config_cu_name + " process already started.")

    def stop(self):
        """
        Public method that stops the data acquisition through a Modbus/TCP communication.

        :return: N/A
        """
        if self.process_started:
            if self.client.is_open():
                self.client.close()
            self.__updateComStatus(CuStatus.UNKNOWN)
            display_message = "================================\n" + \
                              self.config_cu_name + " Life counter process stopped\n" \
                              "================================\n"
            self.__displayLog(display_message)
            self.thread.cancel()
            self.__notifyStop()
            self.process_started = False
        else:
            showinfo(self.config_cu_name + " info", self.config_cu_name + " process already stopped.")

    def __updateComStatus(self, status):
        """
        Private method that allows to ask the GUI related object ot update its CU status picture.

        :param status: (Enum CuStatus) Status of the CU communication
        :return: N/A
        """
        self.gui.displayCuComStatus(self.config_cu_name, status)

    def __displayLog(self, message):
        """
        Private method used to write logs in the CU frame on the GUI.

        :param message: (string) Message to display
        :return: N/A
        """
        self.gui.displayLog(self.config_cu_name, message)

    def __displayError(self, error):
        """
        Private method to generate popup in case of communication error detected.

        :param error: (string) Message to display on the popup
        :return:N/A
        """
        showerror("Error", error)

    def __notifyRunning(self):
        """
        Private method to generate a log to notify that the process is currently running.

        :return: N/A
        """
        process_current_time = datetime.now()
        process_check_time_delta = process_current_time - self.previous_process_time
        if (int(process_check_time_delta.total_seconds()) >= self.config_process_check_time) \
                or self.process_startup:
            log_message = self.config_cu_name + " - Process running."
            self.logger.info(log_message)
            self.previous_process_time = datetime.now()
            self.process_startup = False

    def __notifyStop(self):
        """
        Private method to generate a log to notify that the process was stopped

        :return: N/A
        """
        log_message = self.config_cu_name + " - Process stopped."
        self.logger.info(log_message)
        self.logger = None

    def __modbusClientConnection(self):
        """
        Private method that handles the Modbus connection to the CU.

        This method implements the following checks:
        - Maximum connection attempts. If the maximum number is reached, a popup is displayed and the connection is
            aborted. The CU communication status display changes to unhealthy.
        - Connection established. If it is not established, a popup is displayed and a log is written in the CU frame
            and in the log file. The CU communication status display changes to unhealthy.
            If the connection is correctly established, the CU communication status display changes to healthy.
        :return: N/A
        """
        if not self.client.is_open():
            if self.connection_attempt < MAX_CONNECTION_ATTEMPT:
                # Try to connect
                try:
                    if not self.client.open():
                        self.thread.cancel()
                        self.__updateComStatus(CuStatus.UNHEALTHY)
                        # If not able, records the error
                        error_message = "Unable to connect to {} : {}.".format(self.config_server_host,str(SERVER_PORT))
                        log_message = "Unable to connect to {} ({}:{}).".format(self.config_cu_name,
                                                                                self.config_server_host,
                                                                                str(SERVER_PORT))
                        display_message = log_message
                        self.__displayError(error_message)
                        self.__displayLog(display_message)
                        self.logger.error(log_message)
                        self.connection_attempt += 1
                    else:
                        self.__updateComStatus(CuStatus.HEALTHY)
                except AttributeError:
                    pass
            else:
                self.stop()
                self.__displayError("Connection to " + self.config_cu_name + " aborted.")
        else:
            self.__updateComStatus(CuStatus.HEALTHY)

    def __processCheck(self):
        """
        Private method that checks that the counter value of the CU is still changing.

        This method prints the value read in the frame of the CU. If the counter value does not change between two
        calls, an error popup is displayed and the error is written in the log file.

        :return: N/A
        """
        # Counter test
        if self.client.is_open():

            # Read the counter value
            self.counter_value = self.client.read_holding_registers(self.config_register_address)
            display_message = "{} Life counter value: {}".format(self.config_cu_name, str(self.counter_value))
            self.__displayLog(display_message)

            # Test if counter is incremented
            if self.counter_value == self.previous_counter_value or str(self.counter_value) == "None":
                self.thread.cancel()
                self.__updateComStatus(CuStatus.UNHEALTHY)
                error_message = self.config_cu_name + " has stopped running."
                log_message = "Life counter value didn't change (value = {}))".format(self.counter_value)
                display_message = log_message
                self.__displayError(error_message)
                self.__displayLog(display_message)
                self.logger.error(log_message)

            # Records the counter value for next comparison
            self.previous_counter_value = self.counter_value
