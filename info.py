# info.py
from tkinter import *
from tkinter import Label
from tkinter import messagebox
import tkinter as tk
import mysql.connector
import pandas as pd
from filteres1 import Filteres1
from rekapes1 import Rekapes1
from visualrekap import Visualrekap
from visualfilter import Visualfilter


class Info:
    def __init__(self, root):
        self.conn = mysql.connector.connect(
            host="localhost", username="root", password="admin", database="keruneg")

        if self.conn.is_connected():
            print("Connected to MySQL Workbench!")

        # Buat atribut cursor di dalam objek Keruneg
        self.cursor = self.conn.cursor()

        self.root = root
        self.root.title("Informasi Umum")
        self.root.geometry("1350x760+0+0")

        lbltitle = Label(self.root, bd=20, relief=RIDGE, text="INFORMASI UMUM",
                         fg="red", bg="white", font=("times new roman", 30, "bold"))
        lbltitle.pack(side=TOP, fill=X)

        # ===================================Dataframe=========================================
        Dataframe = Frame(self.root, bd=10, relief=RIDGE)
        Dataframe.place(x=0, y=100, width=1350, height=550)

        DataframeLeft1 = LabelFrame(Dataframe, bd=5, padx=10, relief=RIDGE,
                                    font=("arial", 12, "bold"), text="Filter Per Eselon I")
        DataframeLeft1.place(x=5, y=5, width=610, height=300)

        DataframeRight1 = LabelFrame(Dataframe, bd=5, padx=10, relief=RIDGE,
                                     font=("arial", 12, "bold"), text="Rekapitulasi")
        DataframeRight1.place(x=620, y=5, width=700, height=260)

        DataframeLeft2 = LabelFrame(Dataframe, bd=5, padx=10, relief=RIDGE,
                                    font=("arial", 12, "bold"), text="Multilevel PieChart")
        DataframeLeft2.place(x=5, y=305, width=610, height=220)

        DataframeRight2 = LabelFrame(Dataframe, bd=5, padx=10, relief=RIDGE,
                                     font=("arial", 12, "bold"), text="Rekap Diagram")
        DataframeRight2.place(x=620, y=265, width=700, height=260)

        # ======================= Button Frame ==============
        ButtonFrame = Frame(self.root, bd=10, relief=RIDGE)
        ButtonFrame.place(x=1113, y=650, width=235, height=60)

        btnXls = Button(ButtonFrame, text="Excel", bg="green", fg="white", font=(
            "arial", 10, "bold"), width=12, command=self.Xls)
        btnXls.grid(row=0, column=1)

        btnKeluar = Button(ButtonFrame, text="Keluar", bg="green", fg="white", font=(
            "arial", 10, "bold"), width=12, command=root.destroy)
        btnKeluar.grid(row=0, column=2)

        # =======================Pemanggilan Tampilan ==============
        self.filter_frame = Filteres1(DataframeLeft1)
        self.filter_frame = Visualfilter(DataframeLeft2)

        self.filter_frame = Rekapes1(DataframeRight1)
        self.filter_frame = Visualrekap(DataframeRight2)

        # ======================= Pendefinisian ==============
    def Xls(self):
        query_combined = """
            SELECT temuan.*, keuangan.total, keuangan.ang, keuangan.phs, keuangan.sisa
            FROM temuan
            INNER JOIN keuangan ON temuan.ref = keuangan.ref
        """
        data = self.fetch_data_from_database(query_combined)

        if data:
            # Menyimpan data ke file Excel
            self.create_excel_file(data, 'informasi_umum.xlsx')
            print("Data berhasil disimpan ke informasi_umum.xlsx")

            # Menampilkan dialog sukses
            messagebox.showinfo("Download Excel Sukses!",
                                "File Excel berhasil diunduh.")
        else:
            print("Tidak ada data yang diambil dari database.")

    def fetch_data_from_database(self, query):
        # Mengeksekusi query
        self.cursor.execute(query)

        # Mengambil hasil query
        data = self.cursor.fetchall()

        return data

    def create_excel_file(self, data, excel_file):
        # Membuat DataFrame menggunakan pandas
        df = pd.DataFrame(data, columns=['ref', 'id_sikad', 'jenis_temuan', 'es1', 'satker', 'nama_pj', 'nip', 'jab', 'jenis_kasus',
                                         'jenis_kerugian', 'thn', 'dokumen', 'tgl_dok', 'ket', 'status', 'dok', 'total', 'ang', 'phs', 'sisa'])

        # Menyimpan DataFrame ke file Excel
        df.to_excel(excel_file, index=False)

# root = tk.Tk()
# ob = Info(root)
# root.mainloop()


try:
    root = tk.Tk()
    ob = Info(root)
    root.mainloop()

finally:
    # Close the database connection when the Tkinter window is closed
    if hasattr(ob, 'conn') and ob.conn.is_connected():
        ob.conn.close()
        print("MySQL Connection Closed.")
