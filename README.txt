To compile code to executable with pyinstaller:
- Modify the following file: LifeCounter.spec with the following: hiddenimports=['PIL', 'PIL._imagingtk', 'PIL._tkinter_finder'], 
- Compile with the following command: pyinstaller LifeCounter.spec