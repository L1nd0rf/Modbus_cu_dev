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

	def displayLog(self, log):
		self.text_zone.config(state="normal")
		self.text_zone.insert(END, log + "\n")
		self.text_zone.see(END)
		self.text_zone.config(state="disabled")
		print(log)

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
		
		# Notebook declaration
		self.nb_cu = Notebook(self.gui_main)
		self.nb_cu.grid(row=1, column=0)

		self.cu_process_dic = {}
		for config_dic_id, config_dic_info in self.config_cu.getFullDic().items():
			# Tab declaration for each CU in config
			self.tab = Frame(self.nb_cu, width=300, height=300, padx=5, pady=5)
			self.nb_cu.add(self.tab, text=config_dic_id)
			self.text_zone = Text(self.tab)
			self.text_zone.pack()

			# Status of each CU
			self.cu_process_dic.update({config_dic_id:AcquisitionProcess(config_dic_info, self)})
			# Label(text=config_dic_id).grid()
			# PhotoImage(file="../Modbus_cu_dev/bitmap/state_healthy.gif")

		# Buttons declaration
		Button(self.gui_main, text ='Start', command=lambda: self.cu_process_dic[self.nb_cu.tab(self.nb_cu.select(), "text")].start(), height=2, width=10).grid(row=2, column=0, sticky=W)
		Button(self.gui_main, text ='Stop', command=lambda: self.cu_process_dic[self.nb_cu.tab(self.nb_cu.select(), "text")].stop(), height=2, width=10).grid(row=2, column=0, sticky=E)

		self.gui_main.mainloop()
		
if __name__ == '__main__':
    LifeCounterGui().main()



