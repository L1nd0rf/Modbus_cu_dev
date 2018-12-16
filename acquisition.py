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
import alerts
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
    
    def __init__(self, config, notebook):
        
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
        # self.cu_healthy = AcquisitionProcess.UNKNOWN

        # Logs directory declaration
        if not os.path.exists("../Logs"):
            os.makedirs("../Logs")
        os.chdir("../Logs")

        # GUI textbox declaration
        self.notebook = notebook
        self.tab = Frame(self.notebook, width=300, height=300, padx=5, pady=5)
        self.notebook.add(self.tab, text=self.config_cu_name)
        self.text_zone = Text(self.tab)
        self.text_zone.pack()

    
    def __handleFunction(self):
        self.__processCheck()
        self.thread = Timer(self.config_test_period, self.__handleFunction)
        self.thread.start()

    def start(self):
        if not self.process_started:
            # self.cu_healthy = AcquisitionProcess.HEALTHY
            self.text_zone.config(state="normal")
            self.text_zone.config(state="disabled")
            display_message = self.config_cu_name + " Life counter process started\n================================"
            self.__displayLog(display_message)
            self.thread = Timer(self.config_test_period, self.__handleFunction)
            self.thread.start()
            self.process_started = True
        else:
            showinfo(self.config_cu_name + " info", self.config_cu_name + " process already started.")

    def stop(self):
        if self.process_started:
            # self.cu_healthy = AcquisitionProcess.UNKNOWN
            display_message = "\n" + self.config_cu_name + " Life counter process stopped\n================================\n"
            self.__displayLog(display_message)
            self.thread.cancel()
            self.process_started = False
        else:
            showinfo(self.config_cu_name + " info", self.config_cu_name + " process already stopped.")

    def getCuState():
        return self.cu_healthy
    
    def __displayLog(self, log):
        self.text_zone.config(state="normal")
        self.text_zone.insert(END, log + "\n")
        self.text_zone.see(END)
        self.text_zone.config(state="disabled")
        print(log)

    def __writeLog(self, day_log_file, log_message):
        with open(day_log_file, "a") as log_file:
            log_file.write(log_message)

    def __displayError(self, error):
        # self.cu_healthy = AcquisitionProcess.UNHEALTHY
        self.stop()
        alerts.popup(self.tab, error) 

    def __processCheck(self):

        # Define new name for alarms tracking file, changes everyday
        ############################################################
        day_file_name = "{}-{}_logs.txt".format(time.strftime("%Y_%m_%d"), self.config_cu_name)
        
        # Notify if process still running
        ################################
        process_current_time = datetime.now()
        process_check_time_delta = process_current_time - self.previous_process_time
        if (int(process_check_time_delta.total_seconds()) >= self.config_process_check_time) or self.process_startup == True:
            log_message = "[INFO]   {} // Process running.\n".format(time.strftime("%d/%m/%Y - %H:%M:%S"))
            self.__writeLog(day_file_name, log_message)
            self.previous_process_time = datetime.now()
            self.process_startup = False
            
        # Open or reconnect TCP to server
        #################################
        if not self.client.is_open():
            # Try to connect
            if not self.client.open():
                # If not able, records the error
                error_message = "Unable to connect to {} : {}.".format(self.config_server_host,str(SERVER_PORT))
                log_message = "[ALARM]  {} // Unable to connect to {} ({}):{}.\n".format(time.strftime("%d/%m/%Y - %H:%M:%S"), self.config_cu_name, self.config_server_host,str(SERVER_PORT))
                display_message = log_message
                self.__displayError(error_message)
                self.__displayLog(log_message)
                self.__writeLog(day_file_name, log_message)
               
        
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
                self.__writeLog(day_file_name, log_message)
                
            # Records the counter value for next comparison 
            self.previous_counter_value = self.counter_value




  

    
