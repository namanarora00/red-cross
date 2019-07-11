import sys
import sqlite3
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

from db.db import item, beneficiery, distribution, distributed
from utils.gui_utils import *

from tabs.item_select import SelectItem
from tabs.tools import Tools

from .distribution_detail import DistributionDetail
from .benef_detail import BenefDetail


class Home:
    def __init__(self, parent):
        '''
            This is the main class for the home page. Contains the following tabs:
                1. Item Management.
                2. Beneficiary Details
                3. Distribution history.
                4. Beneficiary distribution history.
                5. Start Distribution. (Select Item tab)
                6. Tools tab.

            Some tabs are explicity written here.
            While others are written as separate classes in different modules.

            Method with prefix `init` initalizes the tree specified by the rest of its name.
            Meaning `init_item_tree` makes a Tree widget in the `item` frame.

            Every Tab has the following components:

                Frame - Each tab is assosciated with a frame which holds all the
                        widgets in the tab.

                Widgets - Widgets in the Tab include a Tree which shows relevant data to the tab.
                          Also there are some other widgets like buttons and text fields.

                Methods - For every tab there are generally 4 methods defined.
                            1. Initalize the frame
                            2. Add the frame as a tab to the window
                            3. Show data in the tree. (and update data)
                            4. Event listeners for button press.
        '''

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

        # Notebook is a container for all the tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.place(relx=0.008, rely=0.014,
                            relheight=0.964, relwidth=0.981)

        self.notebook.configure(width=1192)
        self.notebook.configure(takefocus="")

        # Inits all the tabs
        self.init_item_tree()
        self.init_benef_tree()
        self.init_select_item_tree()
        self.init_distribution_tree()
        self.init_benef_dist_tree()
        self.init_tools_frame()

    # ---------Tab 1--------------#

    def init_item_tree(self):
        '''
            Init method for items tab
        '''

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

        self.update_button = tk.Button(
            self.side_panel, command=self._update_item)
        self.update_button.place(relx=0.060, rely=0.825, height=34,
                                 width=125, bordermode='ignore')
        self.update_button.configure(text='''update''')
        self.update_button.configure(width=125)

        self.delete = tk.Button(self.side_panel, command=self._delete_item)
        self.delete.place(relx=0.515, rely=0.825, height=34,
                          width=125, bordermode='ignore')
        self.delete.configure(text='''Delete''')
        self.delete.configure(width=125)

        self._show_items()

    def _update_item(self):
        '''
            Updates selected item's quantity
        '''
        item_id = None
        try:
            item_id = self.item_tree.selection()[0]
        except IndexError:
            return

        q = self.var_quantity.get()
        if not q:
            messagebox.showerror("Error", "Enter quantity")
            return

        item.execute(f"UPDATE item set quantity='{q}' where id='{item_id}'")

        self.update_item_tree()

    def _show_items(self):
        '''
            Shows item on the tree.
        '''
        data = item.find_by_id()
        for row in data:
            self.item_tree.insert('', 'end', row[0], values=tuple(row))

    def _delete_item(self):
        '''
            Deletes selected item from the tree.
        '''
        try:
            item_id = self.item_tree.selection()[0]
        except IndexError:
            item_id = self.var_id.get()

        if not item_id:
            return

        item.delete_by_id(item_id)
        self.update_item_tree()

    def update_item_tree(self):
        '''
            Updates data to be shown on item tree.
        '''
        self.select_item_ref._show_items()
        self.item_tree.delete(*self.item_tree.get_children())
        self._show_items()

    def _insert_data(self):
        '''
            Insert data to item db on button press.
        '''

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
            self.update_item_tree()

    # ----------- End Tab 1 ----------#

    # ------------ Tab 2 -------------- #

    def init_benef_tree(self):
        self.benef_frame = tk.Frame(self.notebook)
        self.notebook.add(self.benef_frame, padding=3)
        self.notebook.tab(1, text="Beneficiery",
                          compound="left", underline="-1",)

        self.show_benef_detail_button = tk.Button(
            self.benef_frame, command=self._show_benef_detail)
        self.show_benef_detail_button.place(
            relx=0.388, rely=0.008, height=34, width=235)
        self.show_benef_detail_button.configure(
            text='''Show selected Beneficiary''')
        self.show_benef_detail_button.configure(width=235)

        columns = beneficiery._get_column_names()
        columns = [col.upper() for col in columns]

        self.benef_tree = ScrolledTreeView(self.benef_frame)
        self.benef_tree.place(
            relx=0, rely=0.07, relheight=0.946, relwidth=1)
        self.benef_tree.configure(columns=columns)
        self.benef_tree.configure(show="headings")

        for i, column in enumerate(columns):
            self.benef_tree.heading(f"{i}", text=column, anchor="center")
            self.benef_tree.column(f"{i}", width="200")
            self.benef_tree.column(f"{i}", minwidth="20")
            self.benef_tree.column(f"{i}", stretch="1")
            self.benef_tree.column(f"{i}", anchor="w")

        self._show_benef()

    def _show_benef(self):
        '''
            Shows benef data on the tree.
        '''
        data = beneficiery.find_by_id()

        for row in data:
            try:
                self.benef_tree.insert('', 'end', row[0], values=tuple(row))
            except tk.TclError:
                pass

    def _show_benef_detail(self):
        '''
            Creates a new window which shows all the distribution details of
            the beneficiary.
        '''
        try:
            benef = self.benef_tree.selection()[0]
        except IndexError:
            return

        # new window to show benef
        BenefDetail(benef).mainloop()

    # -------- End Tab 2 ---------- #

    # -------- Tab 3 -----------#

    def init_distribution_tree(self):
        self.dist_frame = tk.Frame(self.notebook)
        self.notebook.add(self.dist_frame, padding=3)
        self.notebook.tab(3, text="distributions",
                          compound="left", underline="-1",)

        self.show_dist_detail_button = tk.Button(
            self.dist_frame, command=self._show_dist_detail)
        self.show_dist_detail_button.place(
            relx=0.388, rely=0.008, height=34, width=235)
        self.show_dist_detail_button.configure(
            text='''Show selected Distribution''')
        self.show_dist_detail_button.configure(width=235)

        self.dist_tree = ScrolledTreeView(self.dist_frame)
        self.dist_tree.place(
            relx=0, rely=0.07, relheight=0.946, relwidth=1)
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

    def _show_dist_detail(self):
        try:
            dist = self.dist_tree.selection()[0]
        except IndexError:
            return
        # dist id is first 10 characters of an itemId as stored in the tree
        dist_id = dist[:10]

        # New window to show distribution detail
        DistributionDetail(dist_id).mainloop()

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

    # -------- End Tab 3 ------------ #

    # --------- Tab 4 ------------#

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
        '''
            Shows benef distribution data on the tree.
        '''
        data = distributed.find_by_id()

        for i, row in enumerate(data):
            row = list(row)
            row[3] = datetime.fromtimestamp(int(row[3]))
            try:
                self.benef_dist_tree.insert(
                    '', 'end', i, values=tuple(row))
            except tk.TclError:
                pass

    # ------------ End Tab 4 ----------- #

    # ---------- Tab 5 ------------- #

    def init_select_item_tree(self):
        self.select_item_frame = tk.Frame(self.notebook)
        self.notebook.add(self.select_item_frame, padding=3)
        self.notebook.tab(2, text="select item",
                          compound="left", underline="-1",)

        # this class contains methods for the tab and initializes it
        self.select_item_ref = SelectItem(self.select_item_frame)

    # --------- Tab 6 ------------ #

    def init_tools_frame(self):

        self.tools_frame = tk.Frame(self.notebook)
        self.notebook.add(self.tools_frame, padding=3)
        self.notebook.tab(5, text="Tools",
                          compound="left", underline="-1",)

        # this class contains methods for the tab and initializes it
        self.tools_ref = Tools(self.tools_frame)

    # ----------- End Tab 6 --------- #

    def destroy(self):
        self.notebook.destroy()
