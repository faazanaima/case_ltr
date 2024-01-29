import tkinter as tk
from tkinter import ttk
import mysql.connector


class Filteres1:
    def __init__(self, parent):
        self.root = parent
        self.conn = mysql.connector.connect(
            host="localhost", username="root", password="admin", database="keruneg")
        self.cursor = self.conn.cursor()
        self.FilterEs1 = tk.StringVar()
        self.create_widgets()
        self.populate_table()

    def quick_sort(self, data):
        if len(data) <= 1:
            return data

        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]

        return self.quick_sort(left) + middle + self.quick_sort(right)

    def create_widgets(self):
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Filter ComboBox untuk es1
        self.es1_filter_combobox = ttk.Combobox(
            main_frame, textvariable=self.FilterEs1, width=20)
        self.es1_filter_combobox.grid(
            row=0, column=1, padx=5, sticky="w")

        self.es1_filter_label = ttk.Label(
            main_frame, text="Filter Es1:", anchor="e")
        self.es1_filter_label.grid(
            row=0, column=0, padx=5, sticky="e")

        # Tombol filter
        self.filter_button = ttk.Button(
            main_frame, text="Filter", command=self.filter_data)
        self.filter_button.grid(row=0, column=2, padx=5, pady=5)

        # Treeview untuk menampilkan data
        self.tree = ttk.Treeview(main_frame, columns=(
            "Jenis Temuan", "Jenis Kerugian", "Kasus"), show="headings")
        self.tree.heading("#1", text="Jenis Temuan")
        self.tree.heading("#2", text="Jenis Kerugian")
        self.tree.heading("#3", text="Kasus")

        # Mengatur lebar kolom
        self.tree.column("#1", width=200)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=150)

        # Mengatur tinggi tabel
        self.tree_height = 7
        self.tree['height'] = self.tree_height

        self.tree.grid(row=1, column=0, columnspan=3,
                       padx=5, pady=5, sticky="nsew")

        # Label untuk menampilkan total kasus
        self.total_kasus_label = ttk.Label(main_frame, text="Total Kasus:")
        self.total_kasus_label.grid(
            row=2, column=0, padx=5, sticky="e")

        # Panggil metode update_special_counts untuk menampilkan hitungan khusus
        self.update_special_counts([])

    def update_special_counts(self, filtered_data):
        tp_count = sum(int(data[2])
                       for data in filtered_data if data[1] == "TP")
        tgr_count = sum(int(data[2])
                        for data in filtered_data if data[1] == "TGR")
        pii_count = sum(int(data[2])
                        for data in filtered_data if data[1] == "PIII")

        for record in self.tree.get_children():
            values = self.tree.item(record, 'values')
            if values and values[0] in ["Total TP", "Total TGR", "Total PIII"]:
                self.tree.delete(record)

        self.tree.insert("", "end", values=("", "Total TP", tp_count))
        self.tree.insert("", "end", values=("", "Total TGR", tgr_count))
        self.tree.insert("", "end", values=("", "Total PIII", pii_count))

    def populate_table(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

        self.cursor.execute('SELECT DISTINCT es1 FROM temuan')
        es1_values = [""] + [data[0] for data in self.cursor.fetchall()]
        self.es1_filter_combobox['values'] = es1_values

        self.cursor.execute(
            'SELECT jenis_temuan, jenis_kerugian, COUNT(*) AS kasus FROM temuan GROUP BY jenis_temuan, jenis_kerugian')
        all_data = self.cursor.fetchall()

        filtered_data = [
            data for data in all_data if self.FilterEs1.get().lower() in data[0].lower()]

        sorted_data = self.quick_sort(filtered_data)

        for idx, data in enumerate(sorted_data, start=1):
            self.tree.insert("", "end", iid=idx, values=(
                data[0], data[1], data[2]))

        total_kasus = sum(int(data[2]) for data in sorted_data)
        self.total_kasus_label.config(text=f"Total Kasus: {total_kasus}")

        self.update_special_counts(sorted_data)

    def filter_data(self):
        es1_filter = self.FilterEs1.get()

        if es1_filter:
            if es1_filter.lower() == "lainnya":
                self.cursor.execute(
                    'SELECT jenis_temuan, jenis_kerugian, COUNT(*) AS kasus FROM temuan GROUP BY jenis_temuan, jenis_kerugian')
            else:
                self.cursor.execute(
                    'SELECT jenis_temuan, jenis_kerugian, COUNT(*) AS kasus FROM temuan WHERE es1 = %s GROUP BY jenis_temuan, jenis_kerugian', (es1_filter,))
        else:
            self.cursor.execute(
                'SELECT jenis_temuan, jenis_kerugian, COUNT(*) AS kasus FROM temuan GROUP BY jenis_temuan, jenis_kerugian')

        self.data = self.cursor.fetchall()

        for record in self.tree.get_children():
            self.tree.delete(record)

        for idx, data in enumerate(self.data, start=1):
            self.tree.insert("", "end", iid=idx, values=(
                data[0], data[1], data[2]))

        total_kasus = sum(int(data[2]) for data in self.data)
        self.total_kasus_label.config(text=f"Total Kasus: {total_kasus}")

        self.update_special_counts(self.data)

    def get_data_for_pie_chart(self):
        self.cursor.execute(
            'SELECT jenis_temuan, COUNT(*) AS kasus FROM temuan GROUP BY jenis_temuan')
        pie_chart_data = dict(self.cursor.fetchall())
        return pie_chart_data


if __name__ == "__main__":
    root = tk.Tk()
    ob = Filteres1(root)
    root.mainloop()
