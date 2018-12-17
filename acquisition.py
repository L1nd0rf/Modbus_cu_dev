###########
# Imports #
###########

import time
import os
import sys
from pyModbusTCP.client import ModbusClient
from datetime import datetime
from threading import Event, Thread, Timer
from tkinter import *
from tkinter.messagebox import *
# import alerts
import logging

#############
# Constants #
#############

SERVER_PORT = 502

####################
# Class definition #
####################

class AcquisitionProcess():

    ###############
    # Constructor #
    ############### 
    
    def __init__(self, config, gui):
        
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

        # Values initalization
        self.previous_counter_value = -1
        self.previous_process_check = 0
        self.previous_process_time = datetime.now()
        self.process_startup = True
        self.process_started = False

        # GUI textbox declaration
        self.gui = gui

    
    
    def __handleFunction(self):

        # Define new name for alarms tracking file, changes everyday
        ############################################################
        self.day_file_name = "{}-{}_logs.txt".format(time.strftime("%Y_%m_%d"), self.config_cu_name)

        # Logger decaration
        ###################
        logging.basicConfig(filename="./Logs/" + self.day_file_name)
        
        # Notify if process still running
        #################################
        self.__notifyRunnning()

        # Open or reconnect TCP to server
        #################################
        self.__modbusClientConnection()

        # Check that CU is still running 
        ################################
        self.__processCheck()

        # Handle thread
        ###############
        self.thread = Timer(self.config_test_period, self.__handleFunction)
        self.thread.start()


    def start(self):
        if not self.process_started:
            display_message = self.config_cu_name + " Life counter process started\n================================"
            self.__displayLog(display_message)
            self.thread = Timer(self.config_test_period, self.__handleFunction)
            self.thread.start()
            self.process_started = True
        else:
            showinfo(self.config_cu_name + " info", self.config_cu_name + " process already started.")


    def stop(self):
        if self.process_started:
            self.__updateComStatus("UNKNOWN")
            display_message = "\n" + self.config_cu_name + " Life counter process stopped\n================================\n"
            self.__displayLog(display_message)
            self.thread.cancel()
            self.process_started = False
        else:
            showinfo(self.config_cu_name + " info", self.config_cu_name + " process already stopped.")

    def __updateComStatus(self, status):
        self.gui.displayCuComStatus(self.config_cu_name, status)

    def __writeLog(self, day_log_file, log_message):
        with open(day_log_file, "a") as log_file:
            log_file.write(log_message)


    def __displayLog(self, message):
        self.gui.displayLog(self.config_cu_name, message)


    def __displayError(self, error):
        self.stop()
        showerror("Error", error)


    def __notifyRunnning(self):
        process_current_time = datetime.now()
        process_check_time_delta = process_current_time - self.previous_process_time
        if (int(process_check_time_delta.total_seconds()) >= self.config_process_check_time) or self.process_startup == True:
            log_message = "[INFO]   {} // Process running.\n".format(time.strftime("%d/%m/%Y - %H:%M:%S"))
            logging.info(log_message)
            self.previous_process_time = datetime.now()
            self.process_startup = False


    def __modbusClientConnection(self):
        if not self.client.is_open():
            # Try to connect
            if not self.client.open():
                # If not able, records the error
                error_message = "Unable to connect to {} : {}.".format(self.config_server_host,str(SERVER_PORT))
                log_message = "[ALARM]  {} // Unable to connect to {} ({}):{}.\n".format(time.strftime("%d/%m/%Y - %H:%M:%S"), self.config_cu_name, self.config_server_host,str(SERVER_PORT))
                display_message = log_message
                self.__displayError(error_message)
                self.__displayLog(display_message)
                self.__updateComStatus("UNHEALTHY")
                logging.error(log_message)
            else:
                self.__updateComStatus("HEALTHY")


    def __processCheck(self):

        # Counter test
        ##############
        if self.client.is_open():
            # Read the counter value  
            self.counter_value = self.client.read_holding_registers(self.config_register_address)
            display_message = "{} Life counter value: {}".format(self.config_cu_name, str(self.counter_value))
            self.__displayLog(display_message)
            # Test if counter is incremented
            if self.counter_value == self.previous_counter_value:
                error_message = self.config_cu_name + " has stopped running."
                log_message = "[ALARM] {} // Life counter value didn't change (value = {}))".format(time.strftime("%d/%m/%Y - %H:%M:%S"), self.counter_value)
                display_message = log_message
                self.__displayError(error_message)
                self.__displayLog(display_message)
                logging.error(log_message)
            # Records the counter value for next comparison 
            self.previous_counter_value = self.counter_value




  

    
