################################################
# XCU Live Counter Alarm Generator with Modbus #
################################################

###########
# Imports #
###########

from CuConfig import *
from GuiManagement import *

####################
# Class definition #
####################


class LifeCounter:
	"""
	Class that handles the main program of Life Counter check.
	"""
	def __init__(self):
		"""
		Class constructor
		"""
		# Object initialization
		self.config_cu = None
		self.gui = None

	def __del__(self):
		"""
		Method called at object deletion.

		Override in order to cancel thread and close communication socket in case.

		:return:
		"""
		self.gui.__del__()

	def main(self):
		"""
		Main method.

		:return: N/A
		"""
		# Configuration Management
		self.config_cu = CuConfig("LifeCounterConfig.ini")

		# GUI Management
		self.gui = GuiManagement(self.config_cu)


# Main method call
if __name__ == '__main__':
	LifeCounter().main()
