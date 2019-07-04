from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from gui_utils import *
from db import beneficiery, distributed


class BenefDetail(tk.Tk):
    def __init__(self, b_id, **kwargs):
        super().__init__()

        self.b_id = b_id
        self.geometry("1043x624")
        self.title("Beneficiary")
        self.update()

        self._get_benef_data()
        self._get_dist_data()
        self.init_components()

    def init_components(self):

        self.Labelframe1 = tk.LabelFrame(self)
        self.Labelframe1.place(relx=0.038, rely=0.0,
                               relheight=0.232, relwidth=0.949)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Distribution''')
        self.Labelframe1.configure(width=990)

        self.Label1 = tk.Label(self.Labelframe1)
        self.Label1.place(relx=0.04, rely=0.207, height=24,
                          width=22, bordermode='ignore')
        self.Label1.configure(text='''ID''')

        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.111, rely=0.207, height=24,
                          width=129, bordermode='ignore')
        self.Label2.configure(text=self._benef[0])
        self.Label2.configure(width=129)

        self.Label3 = tk.Label(self.Labelframe1)
        self.Label3.place(relx=0.556, rely=0.207, height=24,
                          width=140, bordermode='ignore')
        self.Label3.configure(text='''Last Distributed''')

        self.Label4 = tk.Label(self.Labelframe1)
        self.Label4.place(relx=0.707, rely=0.207, height=24,
                          width=249, bordermode='ignore')
        self.Label4.configure(text=self._last_dist)
        self.Label4.configure(width=249)

    def init_tree_view(self, data):
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

        for i, row in enumerate(data):
            row = list(row)
            row[3] = datetime.fromtimestamp(int(row[3]))
            try:
                self.benef_dist_tree.insert(
                    '', 'end', i, values=tuple(row))
            except tk.TclError:
                pass

    def _get_benef_data(self):
        benef = beneficiery.find_by_id(self.b_id)

        if benef is None:
            messagebox.showerror("Error", "Beneficiary doesn't exists")
            self.destroy()

        self._benef = benef

    def _get_dist_data(self):
        data = distributed.execute(
            f"select * from distributed where bid='{self.b_id}' order by -timestamp")

        if data:
            self._last_dist = datetime.fromtimestamp(int(data[0][3]))
        else:
            data = []
            self._last_dist = "NA"
        self.init_tree_view(data)


if __name__ == '__main__':
    BenefDetail("5500100034").mainloop()
