import tkinter as tk
from tkinter import ttk, messagebox

import sys

from db.db import *
from utils.gui_utils import *
from windows.distribution import Distribution


class SelectItem():
    def __init__(self, parent):
        self.parent = parent
        self.style = ttk.Style()

        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', background=bgcolor)
        self.style.configure('.', foreground=fgcolor)
        self.style.map('.', background=[
                       ('selected', compcolor), ('active', ana2color)])

        self.init_select_items()
        self._show_items()

    def init_select_items(self):

        self.select_item_tree = ScrolledTreeView(self.parent)
        self.select_item_tree.place(
            relx=0.077, rely=0.069, relheight=0.78, relwidth=0.54)
        self.select_item_tree.configure(columns=["Quantity", "Name"])
        self.select_item_tree.configure(show="headings")

        for i, column in enumerate(["Quantity", "Name"]):
            self.select_item_tree.heading(
                f"#{i+1}", text=column, anchor="center")
            self.select_item_tree.column(f"#{i+1}", width="200")
            self.select_item_tree.column(f"#{i+1}", minwidth="20")
            self.select_item_tree.column(f"#{i+1}", stretch="1")
            self.select_item_tree.column(f"#{i+1}", anchor="w")

        self.start_button = tk.Button(
            self.parent, command=self._start_distribution)
        self.start_button.place(relx=0.656, rely=0.43, height=34, width=235)
        self.start_button.configure(
            text='''Start with selected items''')
        self.start_button.configure(width=235)

    def _show_items(self):
        self.select_item_tree.delete(*self.select_item_tree.get_children())

        data = item.execute("select quantity, name from item")
        for row in data:
            try:
                self.select_item_tree.insert(
                    '', 'end', row[1], values=tuple(row))
            except tk.TclError:
                pass

    def _start_distribution(self):
        selections = self.select_item_tree.selection()  # names of items selected

        if not len(selections):
            messagebox.showerror("error", "Please select at least one item!")
            return

        self.parent.master.master.next_frame(Distribution, selections)

        # init new distribution object with the items
        # init a new frame
        # print()
