
from tkinter.ttk import *
from tkinter import *
import PIL.Image, PIL.ImageTk
from AcquisitionProcess import *


class GuiManagement:

    def __init__(self, config_cu):
        self.text_zone_log = None
        self.pic_com_status = None
        self.gui_main = None
        self.nb_cu = None
        self.config_cu = config_cu
        self.cu_gui_dic = {}
        self.cu_process_dic = {}
        self.cu_tab_dic = {}
        self.gui_row = 0

        self.initMainWindow()
        self.initNotebook()
        self.initCuDictionary()
        self.initButton("Start",
                        lambda: self.cu_process_dic[self.nb_cu.tab(self.nb_cu.select(), "text")].start(),
                        W,
                        self.gui_row,
                        0)
        self.initButton("Stop",
                        lambda: self.cu_process_dic[self.nb_cu.tab(self.nb_cu.select(), "text")].stop(),
                        E,
                        self.gui_row,
                        19)
        self.guiRun()

    def displayLog(self, cu, log):
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

        self.cu_gui_dic[cu].update({"Com Status Picture": self.pic_com_status})
        self.cu_gui_dic[cu]["Picture canvas"].create_image(15, 15, image=self.cu_gui_dic[cu]["Com Status Picture"])
        self.cu_gui_dic[cu]["Picture canvas"].grid(row=self.cu_gui_dic[cu]["Com Status Picture Row"],
                                                   column=1,
                                                   sticky=W)

    def initMainWindow(self):
        self.gui_main = Tk()
        self.gui_main.title("CU life counter")

    def initNotebook(self):
        self.nb_cu = Notebook(self.gui_main)
        self.nb_cu.grid(row=self.gui_row, column=0, columnspan=20)
        self.gui_row += 1


    def initCuLabel(self):
        Label(self.gui_main, text="CU").grid(row=self.gui_row, column=0, sticky=W)
        Label(self.gui_main, text="Communication status").grid(row=self.gui_row, column=1, sticky=W)
        self.gui_row += 1

    def initFrame(self):
        print("Test")

    def initButton(self, name, action, stick, row, column):
        Button(self.gui_main,
               text=name,
               command=action,
               height=2,
               width=10)\
            .grid(row=row,
                  column=column,
                  sticky=stick)

    def guiRun(self):
        self.gui_main.mainloop()

    def initCuDictionary(self):

        # GUI and communication declaration for each CU in config
        im = PIL.Image.open("./bitmap/state_unknown.png")
        photo = PIL.ImageTk.PhotoImage(im)

        for config_dic_id, config_dic_info in self.config_cu.getFullDic().items():
            # Current CU tab dictionary initialization
            self.cu_tab_dic = {}

            # Tabs dictionary declaration
            self.cu_tab_dic.update({"Tab": Frame(self.nb_cu, width=300, height=300, padx=5, pady=5)})
            self.cu_tab_dic.update({"Text": Text(self.cu_tab_dic["Tab"])})
            self.cu_tab_dic.update({"CU Label": Label(self.gui_main, text=config_dic_id)})
            self.cu_tab_dic.update({"Picture canvas": Canvas(self.gui_main, width=25, height=25)})
            self.cu_tab_dic.update({"Com Status Picture": photo})
            self.cu_tab_dic.update({"Com Status Picture Row": self.gui_row})

            # Current CU label display
            self.cu_tab_dic["Text"].pack()
            self.cu_tab_dic["CU Label"].grid(row=self.gui_row, column=0, sticky=W)

            # Adding tab for each CU
            self.nb_cu.add(self.cu_tab_dic["Tab"], text=config_dic_id)

            # Create dictionary of all CUs dictionaries
            self.cu_gui_dic.update({config_dic_id: self.cu_tab_dic})

            # Communication picture display
            self.displayCuComStatus(config_dic_id, "UNKNOWN")

            # Communication to CU initialization
            self.cu_process_dic.update({config_dic_id: AcquisitionProcess(config_dic_info, self)})

            # Incrementing the row to display communication status
            self.gui_row += 1


