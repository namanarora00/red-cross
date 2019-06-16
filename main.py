import tkinter as tk
import sqlite3

from start import Welcome
from home import Home


class Main(tk.Tk):
    '''
        This class is the top level window for all frames.
    '''

    def __init__(self, frames=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if frames is None:
            self.frames = []
        else:
            self.frames = frames

        self.title("Application")
        self.geometry("600x600")

        self.configure(background="#d9d9d9")
        self.configure(highlightbackground="#d9d9d9")
        self.configure(highlightcolor="black")

        self.current_frame = Welcome(self)
        self.update()

    def next_frame(self):
        self.current_frame.destroy()
        self.current_frame = Home(self)

    def destroy(self):
        # commits changes to database before quitting
        sqlite3.connect("cross.db").commit()

        return super().destroy()


if __name__ == "__main__":
    window = Main()
    window.mainloop()
