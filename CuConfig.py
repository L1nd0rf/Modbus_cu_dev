###########
# Imports #
###########

import sys
import ipaddress
from configparser import ConfigParser


class CuConfig():
    """
    Class that allows to parse a configuration (ini file) for a communication witha CU that contains the following
        pattern:
        [CU1]
        CU_NAME = XCU
        # IPV4 (XXX.XXX.XXX.XXX)
        IP = 10.130.13.20
        # In seconds (float or real)
        TEST_PERIOD = 2
        # Modbus register to read(integer)
        REGISTER_ADDRESS = 8192
        # In seconds, higher or equal to TEST_PERIOD (integer)
        PROCESS_CHECK_TIME = 300
    """

    def __init__(self, config_file):
        """
        CuConfig class constructor.

        :param config_file: (String) Config file name (ini file)
        """

        # Import parameters
        self.config_file = config_file

        # Config dictionary initialization
        self.config_dic = {}

        # Config parser Initialization
        self.config = ConfigParser()

        # Read config file
        self.config.read(self.config_file)

        # Parse config file and add each field to the CU config dictionary
        for self.section in self.config.sections():

            # Dictionary initialization for each CU in the config file
            self.dic = {}

            # Parse the fields for the current CU
            self.__getCuName()
            self.__getServerHost()
            self.__getTestperiod()
            self.__getRegisterAddress()
            self.__getProcessCheckTime()

            # Add self.dic to the global CU config dictionary
            self.config_dic.update({self.config[self.section]["CU_NAME"]:self.dic})

    def __getCuName(self):
        """
        Private method to get the CU name from config file.

        :return:
        """
        self.dic["cu_name"] = self.config[self.section]["CU_NAME"]

    def __getServerHost(self):
        """
        Private method to get the server host name from config file.

        :return:
        """
        # Test IPV4 format
        try:
            self.dic["server_host"] = str(ipaddress.ip_address(self.config[self.section]["IP"]))
        except:
            print("Wrong IP address format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)

    def __getTestperiod(self):
        """
        Private method to get the test period from config file.

        :return:
        """
        # Test test period format
        try:
            self.dic["test_period"] = float(self.config[self.section]["TEST_PERIOD"])
        except TypeError:
            print("Wrong test period format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)

    def __getRegisterAddress(self):
        """
        Private method to get the Modbus register address to read from config file.

        :return:
        """
        # Test register address format
        try:
            self.dic["register_address"] = int(self.config[self.section]["REGISTER_ADDRESS"])
        except:
            print("Wrong register address format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)

    def __getProcessCheckTime(self):
        """
        Private method to get the period to check if the process is still running from config file.

        :return:
        """
        # Test process check time format
        try:
            self.dic["process_check_time"] = int(self.config[self.section]["PROCESS_CHECK_TIME"])
        except:
            print("Wrong process check time format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)
    
    def getCuName(self, cu):
        """
        Public method that returns the CU name given the global dictionary cu field.

        :param cu: (string) CU field (from global dictionary)
        :return: (string) CU name
        """
        return self.config_dic[cu]["cu_name"]

    def getCuDic(self, cu):
        """
        Public method that returns the CU dictionary containing the communication and test parameters given the global
        dictionary cu field.

        :param cu: (string) CU field (from global dictionary)
        :return: (dictionary) CU dictionary.
        """
        return self.config_dic[cu]

    def getFullDic(self):
        """
        Public method that returns the global CU dictionary containing all CU dictionaries.

        :return: (dictionary) Global CU dictionary.
        """
        return self.config_dic
