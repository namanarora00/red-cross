import tkinter as tk
import sqlite3

from windows.start import Welcome
from windows.home import Home

from tkinter import Image

# to avoid hidden import in pyinstaller
import PIL

class Main(tk.Tk):
    '''
        This class is the top level window for all frames.
    '''

    def __init__(self, frames=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Application")
        self.geometry("600x600")

        self.configure(background="#d9d9d9")
        self.configure(highlightbackground="#d9d9d9")
        self.configure(highlightcolor="black")

        self.current_frame = Welcome(self)
        self.update()

    def next_frame(self, frame=None, *args, **kwargs):
        '''
            Changes frame to the given frame if provided. Else goes to the `Home frame`
        '''
        self.current_frame.destroy()
        if frame is None:
            self.current_frame = Home(self)
        else:
            self.current_frame = frame(self, *args, **kwargs)

    def destroy(self):
        # commits changes to database before quitting
        sqlite3.connect("cross.db").commit()

        return super().destroy()


if __name__ == "__main__":
    window = Main()
    window.mainloop()
