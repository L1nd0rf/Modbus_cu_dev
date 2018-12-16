from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'D:\Users\aroge\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\Users\aroge\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

setup(
    name = "LifeCounterChecker",
    version = "2",
    description = "Life Counter Checker",
    executables = [Executable("LifeCounterCheck.py")]
)