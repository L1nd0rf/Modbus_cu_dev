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
		self.config_cu = None
		self.gui = None

	def main(self):
		############################
		# Configuration Management #
		############################
		self.config_cu = CuConfig("LifeCounterConfig.ini")

		###################
		# GUI declaration #
		###################

		self.gui = GuiManagement(self.config_cu)
		self.gui.main()


if __name__ == '__main__':
	LifeCounterGui().main()



