import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename

from utils import read_csv
from meta import Table
from admin_utils import initalize

from barcode_util import generate_barcode
from db import beneficiery


class Welcome(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.style = ttk.Style()
        self.style.theme_use("default")

        self.heading = ttk.Label(
            self, text="Welcome!",  font=("Helvetica", 16))
        self.heading.place(rely=0.05, relx=0.417)

        font13 = "-family {Noto Sans CJK JP} -size 12 -weight normal "  \
            "-slant roman -underline 0 -overstrike 0"

        self.welcome_message = tk.Message(self)
        self.welcome_message.place(relx=0.017, rely=0.111,
                                   relheight=0.622, relwidth=0.968)

        self.welcome_message.configure(font=font13)
        self.welcome_message.configure(highlightthickness="1")
        self.welcome_message.configure(
            text='''Hello! Welcome to the Application. We're still working on a name. In the meanwhile, click the button below to add or update data.If you've already built a database then you can skip this step''')
        self.welcome_message.configure(width=581)

        self.select_file = ttk.Button(
            self, text="select CSV", command=self._on_select_file)
        self.select_file.place(relx=0.417, rely=0.7,
                               width=120, height=40)

        if beneficiery.exists():
            self.skip_button = ttk.Button(
                self, text="Skip", command=self.parent.next_frame)
            self.skip_button.place(relx=0.417, rely=0.773,
                                   width=120, height=40)

            self.generate_barcodes = ttk.Button(
                self, text="barcodes", command=self._generate_barcodes)
            self.generate_barcodes.place(relx=0.417, rely=0.9,
                                         width=120, height=40)

        self.pack(fill=tk.BOTH, expand=1)
        self.update()

        initalize()

    def _on_select_file(self):
        path_to_file = askopenfilename()

        if path_to_file:
            self.parse_file(path_to_file)

    def _generate_barcodes(self):
        benefs = beneficiery.find_by_id()
        for b in benefs:
            try:
                # throws illegal character error if ID is not provided
                generate_barcode(b[0])
            except:
                pass

    def parse_file(self, filepath):

        if not filepath.endswith(".csv"):
            messagebox.showerror("Error", "Please choose a valid CSV file")
            return

        try:
            data = read_csv(file_path=filepath)
            columns = data[0].keys()
            if not beneficiery.exists():
                beneficiery.init_table(columns)
                messagebox.showinfo("Info", "Building database")

            inserted = 0
            duplicates = 0

            for row_dict in data:
                if beneficiery.insert_row(row_dict):
                    print("inserted")
                    try:
                        generate_barcode(row_dict["id"])
                    except:
                        pass
                    inserted += 1
                else:
                    duplicates += 1

            messagebox.showinfo(
                "Info", f"{inserted} rows inserted, {duplicates} duplicates")

            self.parent.next_frame()

        except TypeError:
            messagebox.showerror("Error", "Please choose a valid CSV file")


if __name__ == "__main__":
    root = tk.Tk()
    Welcome(root)
    root.mainloop()
