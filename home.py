import tkinter as tk
from tkinter import ttk, messagebox

import platform
import sys
import sqlite3

from meta import Table

item = Table("item")


class Home:
    def __init__(self, parent):

        self.parent = parent

        _bgcolor = '#d9d9d9'
        _fgcolor = '#000000'
        _compcolor = '#d9d9d9'
        _ana1color = '#d9d9d9'
        _ana2color = '#ececec'
        font9 = "-family {DejaVu Sans} -size 10 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        self.style = ttk.Style()

        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[
                       ('selected', _compcolor), ('active', _ana2color)])

        self.parent.geometry("1215x725")

        self.menubar = tk.Menu(self.parent, font=(
            'DejaVu Sans', 10, ), bg=_bgcolor, fg=_fgcolor)
        self.parent.configure(menu=self.menubar)

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=[
                       ('selected', _compcolor), ('active', _ana2color)])

        self.notebook = ttk.Notebook(self.parent)
        self.notebook.place(relx=0.008, rely=0.014,
                            relheight=0.964, relwidth=0.981)

        self.notebook.configure(width=1192)
        self.notebook.configure(takefocus="")

        self.init_item_tree()

    def init_item_tree(self):

        # vars
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_quantity = tk.StringVar()
        self.var_type = tk.StringVar()

        self.item_frame = tk.Frame(self.notebook)
        self.notebook.add(self.item_frame, padding=3)
        self.notebook.tab(0, text="Item", compound="left", underline="-1",)

        self.benef_frame = tk.Frame(self.notebook)
        self.notebook.add(self.benef_frame, padding=3)
        self.notebook.tab(1, text="Beneficiery",
                          compound="left", underline="-1",)

        self.style.configure('Treeview.Heading',  font="TkDefaultFont")

        self.item_tree = ScrolledTreeView(self.item_frame)
        self.item_tree.place(
            relx=0.252, rely=0.03, relheight=0.946, relwidth=0.723)
        self.item_tree.configure(columns="Color size shape item")
        self.item_tree.configure(show="headings")

        self.item_tree.heading("#1", text="Item ID", anchor="center")
        self.item_tree.column("#1", width="200")
        self.item_tree.column("#1", minwidth="20")
        self.item_tree.column("#1", stretch="1")
        self.item_tree.column("#1", anchor="w")

        self.item_tree.heading("#4", text="Quantity", anchor="center")
        self.item_tree.column("#4", width="200")
        self.item_tree.column("#4", minwidth="20")
        self.item_tree.column("#4", stretch="1")
        self.item_tree.column("#4", anchor="w")

        self.item_tree.heading("#2", text="Name", anchor="center")
        self.item_tree.column("#2", width="200")
        self.item_tree.column("#2", minwidth="20")
        self.item_tree.column("#2", stretch="1")
        self.item_tree.column("#2", anchor="w")

        self.item_tree.heading("#3", text="Type", anchor="center")
        self.item_tree.column("#3", width="200")
        self.item_tree.column("#3", minwidth="20")
        self.item_tree.column("#3", stretch="1")
        self.item_tree.column("#3", anchor="w")

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

            self.item_tree.delete(*self.item_tree.get_children())
            self._show_items()


class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported.

        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
            | tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind(
            '<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped


class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''

    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


def _bound_to_mousewheel(event, widget):

    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>',
                       lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):

    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):

    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
