###########
# Imports #
###########

import sys
import ipaddress
from configparser import ConfigParser


class CuConfig():

    def __init__(self, config_file):
        self.config_file = config_file

        # Config dictionary declaration
        self.config = ConfigParser()
        self.config.read(self.config_file)
        self.config_dic = {}
        for self.section in self.config.sections():
            self.dic = {}
            self.__getCuName()
            self.__getServerHost()
            self.__getTestperiod()
            self.__getRegisterAddress()
            self.__getProcessCheckTime()
            self.config_dic.update({self.config[self.section]["CU_NAME"]:self.dic})

    def __getCuName(self):
        self.dic["cu_name"] = self.config[self.section]["CU_NAME"]

    def __getServerHost(self):
        # Test IPV4 format
        try:
            self.dic["server_host"] = str(ipaddress.ip_address(self.config[self.section]["IP"]))
        except:
            print("Wrong IP address format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)

    def __getTestperiod(self):
        # Test test period format
        try:
            self.dic["test_period"] = float(self.config[self.section]["TEST_PERIOD"])
        except:
            print("Wrong test period format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)

    def __getRegisterAddress(self):
        # Test register address format
        try:
            self.dic["register_address"] = int(self.config[self.section]["REGISTER_ADDRESS"])
        except:
            print("Wrong register address format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)

    def __getProcessCheckTime(self):
        # Test process check time format
        try:
            self.dic["process_check_time"] = int(self.config[self.section]["PROCESS_CHECK_TIME"])
        except:
            print("Wrong process check time format for " + self.dic.get("cu_name"))
            input("Press \"Enter\" to quit: ")
            sys.exit(0)
    
    def getCuName(self, cu):
        return self.config_dic[cu]["cu_name"]

    def getCuDic(self, cu):
        return self.config_dic[cu]

    def getFullDic(self):
        return self.config_dic
