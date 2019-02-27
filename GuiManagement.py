###########
# Imports #
###########

from tkinter.ttk import *
from tkinter import *
from tkinter.scrolledtext import *
import PIL.Image, PIL.ImageTk
from AcquisitionProcess import *
from CuStatus import CuStatus
from collections import OrderedDict

####################
# Class definition #
####################


class GuiManagement:
    """
    Class to manage the GUI implementation of the "Life Counter Check" project.

    This class implements:
        - The main window of the GUI;
        - A notebook that contains a tab for each CU in the configuration file (LifeCounterConfig.ini);
        - A connection status for each CU in the configuration file (LifeCounterConfig.ini);
        - A start and a stop button, that will start or stop the acquisition of the currently selected CU (in the
            notebook).
    """
    def __init__(self, config_cu):
        """
        GuiManagement class constructor.

        :param config_cu: (object CuConfig) Object giving access to dictionary with all parameters found in the
            LifeCounterConfig.ini file.
        """
        # Object initialization
        self.text_zone_log = None
        self.pic_com_status = None
        self.gui_main = None
        self.nb_cu = None

        # Dictionaries initialization
        self.cu_gui_dic = {}
        self.cu_process_dic = {}
        self.cu_tab_dic = {}

        # Objects GUI position initialization (depends on number of CUs in config
        self.gui_row = 0

        # Importing CU config
        self.config_cu = OrderedDict(config_cu.getFullDic())

        # Main window definition
        self.__initMainWindow()

        # Dictionary creation with all display parameters for each CU
        self.__initCuDictionary()

        # Starting application
        self.__guiRun()

    def displayLog(self, cu, log):
        """
        Method to display the current logs in the notebook tab corresponding to the CU.

        :param cu: (string) CU name taken from the config dictionary (field "cu_name");
        :param log: (string) Log to display in the frame;
        :return: N/A.
        """

        # Define in which zone to write the log
        self.text_zone_log = self.cu_gui_dic[cu]["Text"]

        # Allow to write in the window
        self.text_zone_log.config(state="normal")

        # Insert log
        self.text_zone_log.insert(END, log + "\n")

        # Show last line written
        self.text_zone_log.see(END)

        # Disable writing mode
        self.text_zone_log.config(state="disabled")

        # print(log)

    def displayCuComStatus(self, cu, status):
        """

        :param cu: (string) CU name taken from the config dictionary (field "cu_name");
        :param status: (enum: CuStatus) Contains a string defining the CU state. Must contain one of the "CuStatus"
            enum values:
        :return: N/A
        """

        if status == CuStatus.HEALTHY:
            self.pic_com_status = PIL.ImageTk.PhotoImage(PIL.Image.open("./bitmap/state_healthy.png"))
        elif status == CuStatus.UNHEALTHY:
            self.pic_com_status = PIL.ImageTk.PhotoImage(PIL.Image.open("./bitmap/state_unhealthy.png"))
        elif status == CuStatus.UNKNOWN:
            self.pic_com_status = PIL.ImageTk.PhotoImage(PIL.Image.open("./bitmap/state_unknown.png"))

        # Update communication picture status and Picture Canvas in CU dictionary
        self.cu_gui_dic[cu].update({"Com Status Picture": self.pic_com_status})
        self.cu_gui_dic[cu]["Picture Canvas"].create_image(15, 15, image=self.cu_gui_dic[cu]["Com Status Picture"])

        # Display picture
        self.cu_gui_dic[cu]["Picture Canvas"].grid(row=self.cu_gui_dic[cu]["Com Status Picture Row"],
                                                   column=1,
                                                   sticky=W)

    def __initMainWindow(self):
        """
        Main window creation (using Tkinter).

        Initialization of all Tkinter objects. The buttons created will react to the press event in order to start the
        counter acquisition.

        :return: N/A
        """
        self.gui_main = Tk()
        self.gui_main.title("CU life counter")
        self.gui_main.resizable(False, False)

        # Calling notebook in main window including a tab for each CU
        self.__initNotebook()

        # Button position definition
        button_row = self.gui_row + len(self.config_cu)

        # Start button calls a lambda function to start the communication of the selected CU (in the notebook).
        # The method called is part of the AcquisitionProcess class.
        self.__initButton("Start",
                          lambda: self.__getCuAcquisitionProcess().start(),
                          W,
                          button_row,
                          0)
        self.__initButton("Stop",
                          lambda: self.__getCuAcquisitionProcess().stop(),
                          E,
                          button_row,
                          19)

    def __initNotebook(self):
        """
        Tkinter notebook initialization.

        :return: N/A
        """
        self.nb_cu = Notebook(self.gui_main)
        self.nb_cu.grid(row=self.gui_row, column=0, columnspan=20)
        self.gui_row += 1

    def __initCuLabel(self):
        """
        Label initialization for the CU status.

        :return: N/A
        """
        Label(self.gui_main, text="CU").grid(row=self.gui_row, column=0, sticky=W)
        Label(self.gui_main, text="Communication status").grid(row=self.gui_row, column=1, sticky=W)
        self.gui_row += 1

    def __initButton(self, name, action, stick, row, column):
        """

        :param name: (string) Name displayed on the button
        :param action: (lambda function) Lambda function to be called when the button is pressed
        :param stick: (N, E, W, S) Sticky parameter (from grid in Tkinter). Accepted values: N, E, W, S.
        :param row: (integer) Row number in the main window.
        :param column: (integer) Column number in the main window.
        :return: N/A
        """
        Button(self.gui_main,
               text=name,
               command=action,
               height=2,
               width=10)\
            .grid(row=row,
                  column=column,
                  sticky=stick)

    def __guiRun(self):
        """
        Method that starts the GUI. Must be called at last.

        :return: N/A
        """
        self.gui_main.mainloop()

    def __getCuAcquisitionProcess(self):
        """
        Private method that returns the Acquisition Process object matching the currently selected CU tab.

        :return: (object AcquisitionProcess) CU acquisition process
        """
        return self.cu_process_dic[self.nb_cu.tab(self.nb_cu.select(), "text")]

    def __initCuDictionary(self):
        """
        Method to create a dictionary for each CU that contains all the GUI parameters.

        This method creates a dictionary for each CU with the following fields:
        - "Tab": Contains a Frame object (from Tkinter) that is added to the notebook previously defined;
        - "Text": Contains a Text object (from Tkinter) that is the tab title;
        - "CU label": Contains a Label object (from Tkinter) that is displayed for the connection status;
        - "Picture Canvas": Contains a Canvas object (from Tkinter) that sets the status picture position;
        - "Com Status Picture": Contains a PhotoImage object (from PIL.ImageTk) that displays the current status of the
            CU;
        - "Com Status Picture Row": Contains an integer that indicates the row of the current CU connection status.

        After the CU parameter dictionary creation, it is added to a global dictionary (cu_gui_dic) that contains all
        CU GUI parameters for all CUs.

        :return: N/A
        """
        # GUI and communication declaration for each CU in config
        im = PIL.Image.open("./bitmap/state_unknown.png")
        photo = PIL.ImageTk.PhotoImage(im)

        for config_dic_id, config_dic_info in self.config_cu.items():
            # Current CU tab dictionary initialization
            self.cu_tab_dic = {}

            # Tabs dictionary declaration
            self.cu_tab_dic.update({"Tab": Frame(self.nb_cu, width=300, height=300, padx=5, pady=5)})
            self.cu_tab_dic.update({"Text": ScrolledText(self.cu_tab_dic["Tab"])})
            self.cu_tab_dic.update({"CU Label": Label(self.gui_main, text=config_dic_id)})
            self.cu_tab_dic.update({"Picture Canvas": Canvas(self.gui_main, width=25, height=25)})
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
            self.displayCuComStatus(config_dic_id, CuStatus.UNKNOWN)

            # Communication to CU initialization
            self.cu_process_dic.update({config_dic_id: AcquisitionProcess(config_dic_info, self)})

            # Incrementing the row to display communication status
            self.gui_row += 1


