import tkinter as tk
from tkinter import ttk, messagebox

import sys

from db import TABLES, beneficiery
from gui_utils import *
from admin_utils import authenticate, add_admin
from barcode_util import generate_barcode


class Tools():
    def __init__(self, parent):
        self.parent = parent
        self.style = ttk.Style()

        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', background=bgcolor)
        self.style.configure('.', foreground=fgcolor)
        self.style.map('.', background=[
                       ('selected', compcolor), ('active', ana2color)])

        self.new_var = tk.StringVar()
        self.admin_var = tk.StringVar()

        self.purge_button = tk.Button(
            self.parent, command=self._purge_database)
        self.purge_button.place(relx=0.142, rely=0.215, height=34, width=205)
        self.purge_button.configure(text='''Purge''')
        self.purge_button.configure(width=205)

        self.generate_barcode_button = tk.Button(
            self.parent, command=self._generate_barcodes)
        self.generate_barcode_button.place(
            relx=0.142, rely=0.314, height=34, width=205)
        self.generate_barcode_button.configure(text='''Barcodes''')
        self.generate_barcode_button.configure(width=205)

        # self.generate_report_button = tk.Button(self.parent)
        # self.generate_report_button.place(
        #     relx=0.568, rely=0.215, height=34, width=205)
        # self.generate_report_button.configure(text='''Reports''')
        # self.generate_report_button.configure(width=205)

        self.new_password_entry = tk.Entry(
            self.parent, textvariable=self.new_var)
        self.new_password_entry.place(
            relx=0.35, rely=0.496, height=26, relwidth=0.225)
        self.new_password_entry.configure(background="white")
        self.new_password_entry.configure(font=font10, show="*")

        self.admin_password_entry = tk.Entry(
            self.parent, textvariable=self.admin_var)
        self.admin_password_entry.place(
            relx=0.35, rely=0.579, height=26, relwidth=0.225)
        self.admin_password_entry.configure(background="white")
        self.admin_password_entry.configure(font=font10, show="*")

        self.add_new_password_button = tk.Button(
            self.parent, command=self._set_new_password)
        self.add_new_password_button.place(
            relx=0.415, rely=0.678, height=34, width=85)
        self.add_new_password_button.configure(text='''Add''')

        self.new_password_label = tk.Label(self.parent)
        self.new_password_label.place(
            relx=0.175, rely=0.496, height=34, width=149)
        self.new_password_label.configure(text='''New Password''')
        self.new_password_label.configure(width=149)

        self.admin_label = tk.Label(self.parent)
        self.admin_label.place(relx=0.208, rely=0.579, height=24, width=99)
        self.admin_label.configure(text='''Admin''')
        self.admin_label.configure(width=99)

        self.heading = tk.Message(self.parent)
        self.heading.place(relx=0.273, rely=0.413,
                           relheight=0.05, relwidth=0.373)
        self.heading.configure(text='''Set up a new admin password''')
        self.heading.configure(width=341)

    def _set_new_password(self):
        if self.admin_var.get() and self.new_var.get():
            if authenticate(self.admin_var.get()):
                add_admin(self.new_var.get())
                messagebox.showinfo("Info", "Added Successfuly")
            else:
                messagebox.showerror("Error", "Wrong password")

    def _purge_database(self):
        go = messagebox.askyesno(
            "Delete", "Are you sure you want to do this? Will erase all database.")

        if go:
            for table in TABLES:
                table.drop()
            messagebox.showinfo("Info", "Application will close now")
            self.parent.master.master.destroy()

    def _generate_barcodes(self):
        benefs = beneficiery.find_by_id()
        for b in benefs:
            try:
                # throws illegal character error if ID is not provided
                generate_barcode(b[0])
            except:
                pass
        messagebox.showinfo(
            "Info", "Generated Barcodes successfully. Find them in `bars` directory")
