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
import PIL.Image, PIL.ImageTk

class LifeCounterGui():
	COM_STATUS = {0 : "HEALTHY",
				  1 : "UNHEALTHY",
				  2 : "UNKNOWN"}

	def displayLog(self, cu, log):
		print (self.cu_gui_dic)
		print(type(cu))
		print (cu)
		self.text_zone_log = self.cu_gui_dic[cu]["Text"]
		self.text_zone_log.config(state="normal")
		self.text_zone_log.insert(END, log + "\n")
		self.text_zone_log.see(END)
		self.text_zone_log.config(state="disabled")
		print(log)

	def displayCuComStatus(self, cu, status):
		if status == "HEALTHY":
			self.pic_com_status = PIL.ImageTk.PhotoImage(PIL.Image.open("./bitmap/state_healthy.png"))
		if status == "UNHEALTHY":
			self.pic_com_status = PIL.ImageTk.PhotoImage(PIL.Image.open("./bitmap/state_unhealthy.png"))
		if status == "UNKNOWN":
			self.pic_com_status = PIL.ImageTk.PhotoImage(PIL.Image.open("./bitmap/state_unknown.png"))
		
		self.cu_gui_dic[cu]["Picture canvas"].create_image(15, 15, image=self.cu_tab_dic["Com Status Picture"])
		# self.cu_gui_dic[cu]["Picture canvas"].grid(row=self.gui_row, column=1, sticky=W)


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
		self.nb_cu.grid(row=1, column=0, columnspan=20)

		# GUI and communication declaration for each CU in config
		self.cu_gui_dic = {}
		self.cu_process_dic = {}
		canvas = []
		im = PIL.Image.open("./bitmap/state_unknown.png")
		photo = PIL.ImageTk.PhotoImage(im)
		Label(self.gui_main, text="CU").grid(row=2, column=0, sticky=W)
		Label(self.gui_main, text="Communication status").grid(row=2, column=1, sticky=W)
		self.gui_row = 3
		for config_dic_id, config_dic_info in self.config_cu.getFullDic().items():
			self.cu_tab_dic = {}
			# Tabs dictionnary declaration
			self.cu_tab_dic.update({"Tab":Frame(self.nb_cu, width=300, height=300, padx=5, pady=5)})
			self.cu_tab_dic.update({"Text":Text(self.cu_tab_dic["Tab"])}) 
			self.cu_tab_dic.update({"CU Label":Label(self.gui_main, text=config_dic_id)})
			self.cu_tab_dic.update({"Picture canvas":Canvas(self.gui_main, width=25, height=25)})
			self.cu_tab_dic.update({"Com Status Picture":photo})

			self.cu_tab_dic["Text"].pack()
			self.cu_tab_dic["CU Label"].grid(row=self.gui_row, column=0, sticky=W)
			
			# Adding tab for each CU
			self.nb_cu.add(self.cu_tab_dic["Tab"], text=config_dic_id)
	
			# Create dictionnary of all CUs dictionnaries
			self.cu_gui_dic.update({config_dic_id:self.cu_tab_dic})

			# Communication picture display
			self.displayCuComStatus(config_dic_id, "UNKNOWN")

			# Communication to each CU
			self.cu_process_dic.update({config_dic_id:AcquisitionProcess(config_dic_info, self)})

			# Incrementing the row to display communication status
			self.gui_row += 1

		# Buttons declaration
		Button(self.gui_main, text ='Start', command=lambda: self.cu_process_dic[self.nb_cu.tab(self.nb_cu.select(), "text")].start(), height=2, width=10).grid(row=self.gui_row, column=0, sticky=W)
		Button(self.gui_main, text ='Stop', command=lambda: self.cu_process_dic[self.nb_cu.tab(self.nb_cu.select(), "text")].stop(), height=2, width=10).grid(row=self.gui_row, column=19, sticky=E)

		self.gui_main.mainloop()
		
if __name__ == '__main__':
    LifeCounterGui().main()



