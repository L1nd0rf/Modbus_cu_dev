################################################
# XCU Live Counter Alarm Generator with Modbus #
################################################

###########
# Imports #
###########

from tkinter import *
from tkinter.ttk import *
from acquisition import *
from configManagement import *

class LifeCounterGui():
	def main(self):
		
		############################
		# Configuration Management #
		############################
		self.config_cu = CuConfig("LifeCounterConfig.ini")

		###################
		# GUI declaration #
		###################
		self.gui_main = Tk()
		self.gui_main.title("CU life counter")
		
		# Tabs declaration
		self.nb_cu = Notebook(self.gui_main)
		self.nb_cu.grid(row=1, column=0)

		# Buttons declaration
		Button(self.gui_main, text ='Start', command=lambda: self.process[self.nb_cu.tab(self.nb_cu.select(), "text")].start(), height=2, width=10).grid(row=2, column=0, sticky=W)
		Button(self.gui_main, text ='Stop', command=lambda: self.process[self.nb_cu.tab(self.nb_cu.select(), "text")].stop(), height=2, width=10).grid(row=2, column=0, sticky=E)
		self.process = {}
		for config_dic_id, config_dic_info in self.config_cu.getFullDic().items():
			self.process.update({config_dic_id:AcquisitionProcess(config_dic_info, self.nb_cu)})
			Label(text=config_dic_id).grid()
			PhotoImage(file="../modbus_dev/bitmap/state_healthy.gif")
		self.gui_main.mainloop()
		
if __name__ == '__main__':
    LifeCounterGui().main()



