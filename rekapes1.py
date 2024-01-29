import tkinter as tk
from tkinter import ttk
import mysql.connector


class Rekapes1:
    def __init__(self, parent):
        self.root = parent
        self.conn = mysql.connector.connect(
            host="localhost", username="root", password="admin", database="keruneg")
        self.cursor = self.conn.cursor()
        self.create_widgets()

    def create_widgets(self):
        tree_frame = ttk.LabelFrame(self.root)
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        title_font = ('Arial', 12, 'bold')
        title_label = ttk.Label(
            tree_frame, text="Tabel Rekapitulasi Data Per Eselon 1", font=title_font, justify="center")
        title_label.grid(row=0, column=0, columnspan=1, pady=(0, 3))

        self.tree = ttk.Treeview(tree_frame, columns=(
            "Es1", "BPK (Eksternal)", "Itjen (Internal)", "Total Kasus"), show="headings")

        bold_style = ttk.Style()
        bold_style.configure("Bold.TLabel", font=('Arial', 16, 'bold'))

        self.tree.heading("Es1", text="Es1", anchor="center",
                          command=lambda: self.sort_column("Es1"))
        self.tree.heading("BPK (Eksternal)", text="BPK (Eksternal)",
                          anchor="center", command=lambda: self.sort_column("BPK (Eksternal)"))
        self.tree.heading("Itjen (Internal)", text="Itjen (Internal)",
                          anchor="center", command=lambda: self.sort_column("Itjen (Internal)"))
        self.tree.heading("Total Kasus", text="Total Kasus", anchor="center",
                          command=lambda: self.sort_column("Total Kasus"))

        self.tree.column("Es1", width=200)
        self.tree.column("BPK (Eksternal)", width=150)
        self.tree.column("Itjen (Internal)", width=150)
        self.tree.column("Total Kasus", width=100)

        self.tree_height = 8
        self.tree['height'] = self.tree_height

        self.cursor.execute('SELECT DISTINCT es1 FROM temuan')
        es1_values = [data[0] for data in self.cursor.fetchall()]

        total_bpk = 0
        total_itjen = 0
        total_kasus = 0

        for es1 in es1_values:
            bpk_count = self.get_jenis_temuan_count(es1, "BPK (Eksternal)")
            itjen_count = self.get_jenis_temuan_count(es1, "Itjen (Internal)")
            total_kasus_row = bpk_count + itjen_count

            self.tree.insert("", "end", values=(
                es1, bpk_count, itjen_count, total_kasus_row))

            total_bpk += bpk_count
            total_itjen += itjen_count
            total_kasus += total_kasus_row

        self.tree.insert("", "end", values=(
            "Total", total_bpk, total_itjen, total_kasus))

        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")
        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def get_jenis_temuan_count(self, es1, jenis_temuan):
        self.cursor.execute(
            'SELECT COUNT(*) FROM temuan WHERE es1 = %s AND jenis_temuan = %s', (es1, jenis_temuan))
        return self.cursor.fetchone()[0]

    def quick_sort(self, items, col):
        if len(items) <= 1:
            return items
        else:
            pivot = self.tree.set(items[0], col)
            lesser = [item for item in items[1:]
                      if self.tree.set(item, col) < pivot]
            greater = [item for item in items[1:]
                       if self.tree.set(item, col) >= pivot]
            return self.quick_sort(lesser, col) + [items[0]] + self.quick_sort(greater, col)

    def sort_column(self, col):
        items = self.tree.get_children('')
        sorted_items = self.quick_sort(items, col)
        self.refresh_treeview(sorted_items)

    def refresh_treeview(self, items):
        for index, item in enumerate(items):
            self.tree.move(item, '', index)


if __name__ == "__main__":
    root = tk.Tk()
    app = Rekapes1(root)
    root.mainloop()
