from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from gui_utils import *
from db import distributed, distribution


class DistributionDetail(tk.Tk):
    def __init__(self, dist_id):
        super().__init__()

        self.dist_id = dist_id

        self.geometry("1043x624")
        self.title("Distribution")

        self.update()

        self._get_data()
        self._get_benefs()
        self.init_components()

    def _get_data(self):
        dist = distribution.find_by_id(self.dist_id)
        print(dist)

        if not dist:
            messagebox.showerror("Error", "Distribution does not exists")
            self.destroy()
            return

        self._items = dist[1]
        self._timestamp = datetime.fromtimestamp(int(dist[2]))

    def _get_benefs(self):
        dists = distributed.find_by_id(self.dist_id, many=True)
        benefs = set()
        self._total_items = len(dists)

        for d in dists:
            benefs.add(d[0])

        self._benefs = len(benefs)

        self.init_tree_view(dists)

    def init_components(self):

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=bgcolor)
        self.style.configure('.', foreground=fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[
                       ('selected', compcolor), ('active', ana2color)])

        self.Labelframe1 = tk.LabelFrame(self)
        self.Labelframe1.place(relx=0.038, rely=0.0,
                               relheight=0.232, relwidth=0.949)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Distribution''')
        self.Labelframe1.configure(width=990)

        self.Label1 = tk.Label(self.Labelframe1)
        self.Label1.place(relx=0.02, rely=0.207, height=24,
                          width=22, bordermode='ignore')
        self.Label1.configure(text='''ID''')

        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.061, rely=0.207, height=24,
                          width=129, bordermode='ignore')
        self.Label2.configure(text=self.dist_id)
        self.Label2.configure(width=129)

        self.Label3 = tk.Label(self.Labelframe1)
        self.Label3.place(relx=0.222, rely=0.207, height=24,
                          width=82, bordermode='ignore')
        self.Label3.configure(text='''Datetime''')

        self.Label4 = tk.Label(self.Labelframe1)
        self.Label4.place(relx=0.313, rely=0.207, height=24,
                          width=249, bordermode='ignore')
        self.Label4.configure(text=self._timestamp)
        self.Label4.configure(width=249)

        self.Label5 = tk.Label(self.Labelframe1)
        self.Label5.place(relx=0.586, rely=0.207, height=24,
                          width=89, bordermode='ignore')
        self.Label5.configure(text='''Items :''')
        self.Label5.configure(width=89)

        self.Label6 = tk.Label(self.Labelframe1)
        self.Label6.place(relx=0.657, rely=0.207, height=24,
                          width=319, bordermode='ignore')
        self.Label6.configure(text=self._items)
        self.Label6.configure(width=319)

        self.Label7 = tk.Label(self.Labelframe1)
        self.Label7.place(relx=0.242, rely=0.621, height=24,
                          width=500, bordermode='ignore')
        self.Label7.configure(
            text=f'''Distributed total {self._total_items} items among {self._benefs} different beneficiaries''')
        self.Label7.configure(width=469)

    def init_tree_view(self, dists):
        columns = distributed._get_column_names()

        self.benef_dist_tree = ScrolledTreeView(self)
        self.benef_dist_tree.place(
            relx=0.038, rely=0.256, relheight=0.712, relwidth=0.949)

        self.benef_dist_tree.configure(columns=columns)
        self.benef_dist_tree.configure(show="headings")

        for i, column in enumerate(columns):
            self.benef_dist_tree.heading(
                f"{i}", anchor="center", text=column)
            self.benef_dist_tree.column(f"{i}", width="190")
            self.benef_dist_tree.column(f"{i}", minwidth="20")
            self.benef_dist_tree.column(f"{i}", stretch="1")
            self.benef_dist_tree.column(f"{i}", anchor="w")

        for i, row in enumerate(dists):
            row = list(row)
            row[3] = datetime.fromtimestamp(int(row[3]))
            try:
                self.benef_dist_tree.insert(
                    '', 'end', i, values=tuple(row))
            except tk.TclError:
                pass

# HIDhqFkjwG


if __name__ == "__main__":
    DistributionDetail("HlDhqFkJwG").mainloop()
