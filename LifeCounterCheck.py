################################################
# XCU Live Counter Alarm Generator with Modbus #
################################################

###########
# Imports #
###########

from CuConfig import *
from GuiManagement import *


class LifeCounterGui:

	def __init__(self):
		# Object initialization
		self.config_cu = None
		self.gui = None

	def main(self):
		# Configuration Management
		self.config_cu = CuConfig("LifeCounterConfig.ini")

		# GUI Management
		self.gui = GuiManagement(self.config_cu)


if __name__ == '__main__':
	LifeCounterGui().main()
