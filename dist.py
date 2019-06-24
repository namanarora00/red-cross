import tkinter as tk
from tkinter import ttk, messagebox

import sys

import db
from gui_utils import *

import random
import string
from datetime import datetime


class Distribution:
    def __init__(self, parent, items):
        self.items = items
        self.parent = parent

        self._create_dist()

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=bgcolor)
        self.style.configure('.', foreground=fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[
                       ('selected', compcolor), ('active', ana2color)])

        self.parent.geometry("1218x749")
        self.parent.title("Distribution")
        self.container = tk.Frame(self.parent)

        self.container.place(relheight=1, relwidth=1, relx=0, rely=0)

        self.style.configure('Treeview.Heading', font="TkDefaultFont")

        self.dist_data_tree = ScrolledTreeView(self.container)
        self.dist_data_tree.place(
            relx=0.008, rely=0.04, relheight=0.713, relwidth=0.468)

        # current distribution's data
        cols = ["beneficiery", "item", "distribution", "timestamp", "quantity"]
        self.dist_data_tree.configure(
            columns=cols)
        self.dist_data_tree.configure(show="headings")
        for i, col in enumerate(cols):
            self.dist_data_tree.heading(f"{i}", text=col)
            self.dist_data_tree.heading(f"{i}", anchor="center")
            self.dist_data_tree.column(f"{i}", width="278")
            self.dist_data_tree.column(f"{i}", minwidth="20")
            self.dist_data_tree.column(f"{i}", stretch="1")
            self.dist_data_tree.column(f"{i}", anchor="w")

        # Items used in current distribution
        self.dist_item_tree = ScrolledTreeView(self.container)
        self.dist_item_tree.place(
            relx=0.484, rely=0.04, relheight=0.286, relwidth=0.501)
        self.dist_item_tree.configure(columns=["item", "quantity"])
        self.dist_item_tree.configure(show="headings")

        self.dist_item_tree.heading("#1", text="item")
        self.dist_item_tree.heading("#1", anchor="center")
        self.dist_item_tree.column("#1", width="298")
        self.dist_item_tree.column("#1", minwidth="20")
        self.dist_item_tree.column("#1", stretch="1")
        self.dist_item_tree.column("#1", anchor="w")

        self.dist_item_tree.heading("#2", text="Quantity")
        self.dist_item_tree.heading("#2", anchor="center")
        self.dist_item_tree.column("#2", width="298")
        self.dist_item_tree.column("#2", minwidth="20")
        self.dist_item_tree.column("#2", stretch="1")
        self.dist_item_tree.column("#2", anchor="w")

        self.manual_frame = tk.LabelFrame(self.container)
        self.manual_frame.place(relx=0.008, rely=0.788,
                                relheight=0.18, relwidth=0.468)
        self.manual_frame.configure(relief='groove')
        self.manual_frame.configure(text='''Manual''')
        self.manual_frame.configure(width=570)

        self.search_benef_button = tk.Button(
            self.manual_frame, command=self.__search_benef)
        self.search_benef_button.place(relx=0.596, rely=0.222, height=34,
                                       width=205, bordermode='ignore')
        self.search_benef_button.configure(text='''Search''')
        self.search_benef_button.configure(width=205)

        self.bid = tk.StringVar()
        self.search_benef_entry = tk.Entry(
            self.manual_frame, textvariable=self.bid)
        self.search_benef_entry.place(relx=0.018, rely=0.222, height=36,
                                      relwidth=0.554, bordermode='ignore')
        self.search_benef_entry.configure(background="white")
        self.search_benef_entry.configure(font=font10)
        self.search_benef_entry.configure(width=316)

        self.close_dist_button = tk.Button(
            self.manual_frame, command=self.close)
        self.close_dist_button.place(relx=0.34, rely=0.667, height=34,
                                     width=250, bordermode='ignore')
        self.close_dist_button.configure(text='''Close Distribution''')
        self.close_dist_button.configure(width=250)

        self.benef_info_frame = tk.LabelFrame(self.container)
        self.benef_info_frame.place(relx=0.484, rely=0.347,
                                    relheight=0.621, relwidth=0.501)
        self.benef_info_frame.configure(relief='groove')
        self.benef_info_frame.configure(text='''Beneficiery''')
        self.benef_info_frame.configure(width=610)

        self.benef_info_list = ScrolledListBox(self.benef_info_frame)
        self.benef_info_list.place(
            relx=0.016, rely=0.086, relheight=0.768, relwidth=0.961, bordermode='ignore')
        self.benef_info_list.configure(background="white")
        self.benef_info_list.configure(font=font10)
        self.benef_info_list.configure(highlightcolor="#d9d9d9")
        self.benef_info_list.configure(selectbackground="#c4c4c4")
        self.benef_info_list.configure(width=10)

        self.dist_button = tk.Button(
            self.benef_info_frame, command=self.__distribute)
        self.dist_button.place(relx=0.344, rely=0.903, height=34,
                               width=205, bordermode='ignore')
        self.dist_button.configure(text='''distribute''')
        self.dist_button.configure(width=205)

        # show data
        self._show_items()
        self._show_dist_record()

    def close(self):
        self.parent.next_frame()

    def inventory(self):
        inv = {}

        for i in self.items:
            q = db.item.execute(
                f"Select quantity from item where name='{i}';")

            if len(q):
                inv[i] = q[0][0]

        return inv

    def _show_items(self):
        self.dist_item_tree.delete(*self.dist_item_tree.get_children())

        inv = self.inventory()

        for i in inv:
            self.dist_item_tree.insert('', 'end', i, values=(i, inv[i]))

    def __search_benef(self):
        benef = db.beneficiery.find_by_id(self.bid.get())
        if benef:
            self._show_benef(benef)
        else:
            while (self.benef_info_list.get(0)):
                self.benef_info_list.delete(0)

    def _show_benef(self, data):
        while (self.benef_info_list.get(0)):
            self.benef_info_list.delete(0)

        cols = db.beneficiery._get_column_names()

        for i in range(len(data)):
            self.benef_info_list.insert(i, f"{cols[i]} -- {data[i]}")

    def _show_dist_record(self):
        self.dist_data_tree.delete(*self.dist_data_tree.get_children())

        try:
            data = db.distributed.execute(
                f"select * from distributed where id='{self.d_id}'")

            for row in data:
                self.dist_data_tree.insert(
                    '', 'end', row[0]+row[1], values=tuple(row))

        except Exception:
            pass

    def __distribute(self):
        inv = self.inventory()
        items = self.dist_item_tree.selection()

        if not len(items):
            items = self.inventory().keys()

        benef = self.benef_info_list.get(0)
        if not benef:
            return
        benef = benef.split('--')[1].strip()

        for i in items:
            d = db.distributed.execute(
                f"select * from distributed where bid='{benef}' and id='{self.d_id}' and item='{i}'  ")

            if d:
                messagebox.showerror("error", "Already distributed")
                return

        for i in items:

            if int(inv[i]) > 0:
                print(inv[i])
                t = str(int(datetime.now().timestamp()))
                if db.distributed.insert_row(
                        {"bid": benef, "timestamp": t, "id": self.d_id, "quantity": "1", "item": i}, force=True):
                    print("done")

        # TODO: refactor to one loop without causing the db to lock
        for i in items:
            if(int(inv[i]) > 0):
                db.item.execute(
                    f"UPDATE item set quantity='{int(inv[i])-1}' where name='{i}'")

        self.__update()

    def __update(self):
        self._show_dist_record()
        self._show_items()

    def _create_dist(self):
        d_id = ''.join(random.sample(string.ascii_letters, 10))
        timestamp = str(int(datetime.now().timestamp()))

        db.distribution.insert_row(
            {"id": d_id, "timestamp": timestamp, "items": ",".join(self.items)})

        self.d_id = d_id

        print("created dist")

    def destroy(self):
        self.container.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Distribution(root, ["food", "bucket"])
    root.mainloop()
