import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED
from tkinter.messagebox import showinfo, showerror, showwarning
import os

class SettingsWindow(tk.Toplevel):
    '''
    This class will create a top level window 
    to select the location of our files
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.dir = r'..\input\\'
        self.files = ['0SOUND.cpk',
                    '0TEXT.cpk',
                    'MSOUND.cpk',
                    'MTEXT.cpk',
                    'OVER.cpk',
                        ]
        self.geometry('400x300')
        self.title('PES2014 PSP Editor Config')
        self.open_btn = ttk.Button(self,
                                text='Open',
                                command=self.open,state=DISABLED)
        self.open_btn.pack()
        ttk.Button(self,
                text='Close',
                command=self.close).pack()
        if (self.checkfiles()):
            self.open_btn.config(state = 'normal')


    def checkfiles(self):
        '''
        Verify if all the needed files are inside the folder 'input'
        '''
        files_in_dir = [x for x in os.listdir(self.dir) if x.endswith(".cpk")]
        if self.files == files_in_dir:
            return True
        return False


    @staticmethod
    def extract_cpk(cpk):
        '''
        Receives the cpk and the dir, then use an external app YACpkTool to extract them
        into a temp folder where we extract our files
        '''
        YACT = r'utils\YACpkTool.exe'
        os.system(YACT + ' '  + cpk)

    def open(self):
        '''
        Extract all cpk files into a temp folder using extract_cpk method and
        deiconify the main app
        '''
        for file in self.files:
            self.extract_cpk(self.dir + file)
        app.deiconify()
        self.destroy()

    def close(self):
        self.destroy()
        app.destroy()


class App(tk.Tk):
    '''
    Our main root app
    '''
    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.title('Main Window')
        self.open_window()


    def open_window(self):
        settings_window = SettingsWindow(self)
        settings_window.grab_set()


if __name__ == '__main__':
    app = App()
    app.withdraw()
    app.mainloop()