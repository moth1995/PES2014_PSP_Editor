import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED
from tkinter.messagebox import showinfo, showerror, showwarning, askokcancel
import os

class SettingsWindow(tk.Toplevel):
    '''
    This class will create a top level window 
    to select the location of our files
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.dir = './input/'
        self.files = ['0SOUND.cpk',
                    '0TEXT.cpk',
                    'MSOUND.cpk',
                    'MTEXT.cpk',
                    'OVER.cpk',
                        ]
        
        self.folders = ['0SOUND',
                    '0TEXT',
                    'MSOUND',
                    'MTEXT',
                    'OVER']
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
        CPKMAKERC = r'utils\cpkmakec.exe'
        cur_dir = os.path.abspath(".")
        os.system(CPKMAKERC + ' \"'  + cpk +'\" -extract=\"' + cur_dir + '/input/' + cpk.split('/')[-1].split('.')[0] + '\"')

    @staticmethod
    def read_header(file):
        '''
        Read the first 4 bytes from a file to recognize and return them
        '''
        with open(file, 'rb') as f:
            return(f.read()[:4])

    @staticmethod
    def get_ext(folder,header):
        '''
        Return extension file according to the header and the folder from where it comes
        '''
        elif  folder == './input/MTEXT' and header == b'\x00\x02\x00\x00': return '.txs'
        elif folder == './input/OVER' and header == b'MWo3': return '.ovl'
        else: return '.bin'

    def open(self):
        '''
        Extract all cpk files into a temp folder using extract_cpk method and
        deiconify the main app
        '''
        for file in self.files:
            self.extract_cpk(self.dir + file)
        # Here we rename to the correct extension of file
        for folder in self.folders:
            files_in_folder = [self.dir + folder + '/' + x for x in os.listdir(self.dir + folder)]
            for file in files_in_folder:
                ext = self.get_ext(self.dir + folder,self.read_header(file))
                try:
                    os.rename(file,file + ext)
                except OSError:
                    showerror(message=f'You must delete files inside the {folder} folder before running the program again\nThe program will close now')
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
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def open_window(self):
        settings_window = SettingsWindow(self)
        settings_window.grab_set()
    def on_closing(self):
        if askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


if __name__ == '__main__':
    app = App()
    app.withdraw()
    app.mainloop()