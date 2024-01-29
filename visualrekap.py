import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualrekap:
    def __init__(self, parent):
        self.root = parent

        # Koneksi ke database
        self.conn = mysql.connector.connect(
            host="localhost", username="root", password="admin", database="keruneg")

        self.cursor = self.conn.cursor()

        self.show_bar_chart()

    def show_bar_chart(self):
        # Ambil data dari database
        self.cursor.execute('SELECT DISTINCT es1 FROM temuan')
        es1_values = [data[0] for data in self.cursor.fetchall()]

        total_kasus_values = []

        # Tambahkan data ke total_kasus_values
        for es1 in es1_values:
            bpk_count = self.get_jenis_temuan_count(es1, "BPK (Eksternal)")
            itjen_count = self.get_jenis_temuan_count(es1, "Itjen (Internal)")
            total_kasus_row = bpk_count + itjen_count
            total_kasus_values.append(total_kasus_row)

        # Apply QuickSort to es1_values and total_kasus_values
        es1_values, total_kasus_values = self.quick_sort(
            es1_values, total_kasus_values)

        # Membuat diagram bar ke atas dengan warna biru tua
        fig, ax = plt.subplots(figsize=(10, 6))
        # Ganti dengan kode warna biru tua yang diinginkan
        ax.bar(es1_values, total_kasus_values, color='#3498db')
        ax.set_ylabel('Total Kasus')
        # ax.set_title('Diagram Bar Ke Atas')

        # Menampilkan diagram bar pada aplikasi tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def get_jenis_temuan_count(self, es1, jenis_temuan):
        self.cursor.execute(
            'SELECT COUNT(*) FROM temuan WHERE es1 = %s AND jenis_temuan = %s', (es1, jenis_temuan))
        return self.cursor.fetchone()[0]

    def quick_sort(self, es1_values, total_kasus_values):
        if len(es1_values) <= 1:
            return es1_values, total_kasus_values
        else:
            pivot = es1_values[0]
            lesser_indices = [i for i, x in enumerate(es1_values) if x < pivot]
            equal_indices = [i for i, x in enumerate(es1_values) if x == pivot]
            greater_indices = [
                i for i, x in enumerate(es1_values) if x > pivot]

            lesser_es1, lesser_total_kasus = self.quick_sort(
                [es1_values[i] for i in lesser_indices], [total_kasus_values[i] for i in lesser_indices])
            equal_es1, equal_total_kasus = self.quick_sort(
                [es1_values[i] for i in equal_indices], [total_kasus_values[i] for i in equal_indices])
            greater_es1, greater_total_kasus = self.quick_sort(
                [es1_values[i] for i in greater_indices], [total_kasus_values[i] for i in greater_indices])

            return lesser_es1 + equal_es1 + greater_es1, lesser_total_kasus + equal_total_kasus + greater_total_kasus


if __name__ == "__main__":
    root = tk.Tk()
    app = Visualrekap(root)
    root.mainloop()
