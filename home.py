import sys
import sqlite3
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

from db import item, beneficiery, distribution, distributed
from gui_utils import *
from item_select import SelectItem


class Home:
    def __init__(self, parent):

        self.parent = parent

        self.style = ttk.Style()

        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', background=bgcolor)
        self.style.configure('.', foreground=fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[
                       ('selected', compcolor), ('active', ana2color)])

        self.parent.geometry("1215x725")

        self.menubar = tk.Menu(self.parent, font=(
            'DejaVu Sans', 10, ), bg=bgcolor, fg=fgcolor)
        self.parent.configure(menu=self.menubar)

        self.style.configure('TNotebook.Tab', background=bgcolor)
        self.style.configure('TNotebook.Tab', foreground=fgcolor)
        self.style.map('TNotebook.Tab', background=[
                       ('selected', compcolor), ('active', ana2color)])

        self.notebook = ttk.Notebook(self.parent)
        self.notebook.place(relx=0.008, rely=0.014,
                            relheight=0.964, relwidth=0.981)

        self.notebook.configure(width=1192)
        self.notebook.configure(takefocus="")

        self.init_item_tree()
        self.init_benef_tree()
        self.init_select_item_tree()
        self.init_distribution_tree()
        self.init_benef_dist_tree()

    def init_select_item_tree(self):
        self.select_item_frame = tk.Frame(self.notebook)
        self.notebook.add(self.select_item_frame, padding=3)
        self.notebook.tab(2, text="select item",
                          compound="left", underline="-1",)

        self.select_item_ref = SelectItem(self.select_item_frame)

    def init_benef_tree(self):
        self.benef_frame = tk.Frame(self.notebook)
        self.notebook.add(self.benef_frame, padding=3)
        self.notebook.tab(1, text="Beneficiery",
                          compound="left", underline="-1",)

        columns = beneficiery._get_column_names()
        columns = [col.upper() for col in columns]

        self.benef_tree = ScrolledTreeView(self.benef_frame)
        self.benef_tree.place(
            relx=0, rely=0.05, relheight=0.946, relwidth=1)
        self.benef_tree.configure(columns=columns)
        self.benef_tree.configure(show="headings")

        for i, column in enumerate(columns):
            self.benef_tree.heading(f"{i}", text=column, anchor="center")
            self.benef_tree.column(f"{i}", width="200")
            self.benef_tree.column(f"{i}", minwidth="20")
            self.benef_tree.column(f"{i}", stretch="1")
            self.benef_tree.column(f"{i}", anchor="w")

        self._show_benef()

    def init_distribution_tree(self):
        self.dist_frame = tk.Frame(self.notebook)
        self.notebook.add(self.dist_frame, padding=3)
        self.notebook.tab(3, text="distributions",
                          compound="left", underline="-1",)

        self.dist_tree = ScrolledTreeView(self.dist_frame)
        self.dist_tree.place(
            relx=0, rely=0.05, relheight=0.946, relwidth=1)
        columns = distribution._get_column_names()

        self.dist_tree.configure(columns=columns)
        self.dist_tree.configure(show="headings")

        for i, column in enumerate(columns):
            self.dist_tree.heading(f"{i}", text=column, anchor="center")
            self.dist_tree.column(f"{i}", width="200")
            self.dist_tree.column(f"{i}", minwidth="20")
            self.dist_tree.column(f"{i}", stretch="1")
            self.dist_tree.column(f"{i}", anchor="w")

        self._show_dist()

    def _show_dist(self):
        data = distribution.find_by_id()

        for row in data:
            row = list(row)
            # format timestamp to date time
            row[2] = datetime.fromtimestamp(int(row[2]))

            try:
                self.dist_tree.insert('', 'end', row[0], values=tuple(row))
            except tk.TclError:
                pass

    def init_benef_dist_tree(self):
        self.benef_dist_frame = tk.Frame(self.notebook)
        self.notebook.add(self.benef_dist_frame, padding=3)
        self.notebook.tab(4, text="history",
                          compound="left", underline="-1",)

        self.benef_dist_tree = ScrolledTreeView(self.benef_dist_frame)
        self.benef_dist_tree.place(
            relx=0, rely=0.05, relheight=0.946, relwidth=1)
        columns = distributed._get_column_names()

        self.benef_dist_tree.configure(columns=columns)
        self.benef_dist_tree.configure(show="headings")

        for i, column in enumerate(columns):
            self.benef_dist_tree.heading(f"{i}", text=column, anchor="center")
            self.benef_dist_tree.column(f"{i}", width="200")
            self.benef_dist_tree.column(f"{i}", minwidth="20")
            self.benef_dist_tree.column(f"{i}", stretch="1")
            self.benef_dist_tree.column(f"{i}", anchor="w")

        self._show_benef_history()

    def _show_benef_history(self):
        data = distributed.find_by_id()

        for i, row in enumerate(data):
            row = list(row)
            row[3] = datetime.fromtimestamp(int(row[3]))
            try:
                self.benef_dist_tree.insert(
                    '', 'end', i, values=tuple(row))
            except tk.TclError:
                pass

    def _show_benef(self):
        data = beneficiery.find_by_id()

        for row in data:
            try:
                self.benef_tree.insert('', 'end', row[0], values=tuple(row))
            except tk.TclError:
                pass

    def init_item_tree(self):

        # vars
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_quantity = tk.StringVar()
        self.var_type = tk.StringVar()

        self.item_frame = tk.Frame(self.notebook)
        self.notebook.add(self.item_frame, padding=3)
        self.notebook.tab(0, text="Item", compound="left", underline="-1",)

        self.style.configure('Treeview.Heading',  font="TkDefaultFont")

        self.item_tree = ScrolledTreeView(self.item_frame)
        self.item_tree.place(
            relx=0.252, rely=0.03, relheight=0.946, relwidth=0.723)

        columns = item._get_column_names()
        columns = map(str.upper, columns)

        self.item_tree.configure(columns=columns)
        self.item_tree.configure(show="headings")

        for i, column in enumerate(columns):
            self.item_tree.heading(f"#{i+1}", text=column, anchor="center")
            self.item_tree.column(f"#{i+1}", width="200")
            self.item_tree.column(f"#{i+1}", minwidth="20")
            self.item_tree.column(f"#{i+1}", stretch="1")
            self.item_tree.column(f"#{i+1}", anchor="w")

        self.side_panel = ttk.LabelFrame(self.item_frame)
        self.side_panel.place(relx=0.002, rely=0.0173,
                              relheight=0.476, relwidth=0.245)
        self.side_panel.configure(text="Item Management")

        self.item_name_label = tk.Label(self.side_panel)
        self.item_name_label.place(relx=0.02, rely=0.127, height=24,
                                   width=105, bordermode='ignore')
        self.item_name_label.configure(text='''Item Name :''')
        self.item_name_label.configure(width=119)

        self.item_name_entry = tk.Entry(
            self.side_panel, textvariable=self.var_name)
        self.item_name_entry.place(relx=0.394, rely=0.127, height=26,
                                   relwidth=0.564, bordermode='ignore')
        self.item_name_entry.configure(background="white")

        self.item_name_entry.configure(width=186)

        self.item_id_label = tk.Label(self.side_panel)
        self.item_id_label.place(relx=0.061, rely=0.254, height=24,
                                 width=79, bordermode='ignore')
        self.item_id_label.configure(text='''Item ID :''')
        self.item_id_label.configure(width=79)

        self.item_id_entry = tk.Entry(
            self.side_panel, textvariable=self.var_id)
        self.item_id_entry.place(relx=0.394, rely=0.254, height=26,
                                 relwidth=0.564, bordermode='ignore')
        self.item_id_entry.configure(background="white")

        self.item_id_entry.configure(selectbackground="#c4c4c4")

        self.item_quantity_entry = tk.Entry(
            self.side_panel, textvariable=self.var_quantity)
        self.item_quantity_entry.place(relx=0.394, rely=0.381, height=26,
                                       relwidth=0.564, bordermode='ignore')
        self.item_quantity_entry.configure(background="white")

        self.item_quantity_entry.configure(selectbackground="#c4c4c4")

        self.item_quantity_label = tk.Label(self.side_panel)
        self.item_quantity_label.place(relx=0.03, rely=0.381, height=24,
                                       width=100, bordermode='ignore')
        self.item_quantity_label.configure(text='''Quantity :''')
        self.item_quantity_label.configure(width=109)

        self.item_type_entry = tk.Entry(
            self.side_panel, textvariable=self.var_type)
        self.item_type_entry.place(relx=0.394, rely=0.508, height=26,
                                   relwidth=0.564, bordermode='ignore')
        self.item_type_entry.configure(background="white")

        self.item_type_entry.configure(selectbackground="#c4c4c4")

        self.item_type_label = tk.Label(self.side_panel)
        self.item_type_label.place(relx=0.02, rely=0.508, height=24,
                                   width=100, bordermode='ignore')
        self.item_type_label.configure(text='''Type :''')
        self.item_type_label.configure(width=119)

        self.search_insert = tk.Button(
            self.side_panel, command=self._insert_data)
        self.search_insert.place(relx=0.06, rely=0.667, height=34,
                                 width=252, bordermode='ignore')
        self.search_insert.configure(text='''Search or Insert''')
        self.search_insert.configure(width=250)

        self.update = tk.Button(self.side_panel)
        self.update.place(relx=0.060, rely=0.825, height=34,
                          width=125, bordermode='ignore')
        self.update.configure(text='''Update''')
        self.update.configure(width=125)

        self.delete = tk.Button(self.side_panel, command=self._delete_item)
        self.delete.place(relx=0.515, rely=0.825, height=34,
                          width=125, bordermode='ignore')
        self.delete.configure(text='''Delete''')
        self.delete.configure(width=125)

        self._show_items()

    def __select(self, *args):
        pass

    def _show_items(self):
        data = item.find_by_id()
        for row in data:
            self.item_tree.insert('', 'end', row[0], values=tuple(row))

    def _delete_item(self):

        try:
            item_id = self.item_tree.selection()[0]
        except IndexError:
            item_id = self.var_id.get()

        if not item_id:
            return

        item.delete_by_id(item_id)

        self.__update()

    def __update(self):
        self.select_item_ref._show_items()
        self.item_tree.delete(*self.item_tree.get_children())
        self._show_items()

    def _insert_data(self):

        if item.find_by_id(self.var_id.get()):
            self.item_tree.selection_set((self.var_id.get()))
            return

        if not self.var_id.get() or not self.var_name.get() or not self.var_quantity.get() or not self.var_type.get():
            messagebox.showerror("Error", "Please specify all fields")
            return

        else:
            row = {}
            row["id"] = self.var_id.get()
            row["name"] = self.var_name.get()
            row["type"] = self.var_type.get()
            row["quantity"] = self.var_quantity.get()

            item.insert_row(row)
            messagebox.showinfo("Info", "Inserted element")
            self.__update()

    def destroy(self):
        self.notebook.destroy()
