from tkinter import *
from tkinter import ttk, filedialog, messagebox, Label, Entry, Button, StringVar
import tkinter as tk
from datetime import datetime
import tkinter
import mysql.connector
import matplotlib.pyplot as plt


class MainApp:
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            messagebox.showerror(
                "Error", "Pilih file dokumen terlebih dahulu.")
            return
        self.Dok.set(file_path)

    def __init__(self, root):
        self.conn = mysql.connector.connect(
            host="localhost", username="root", password="admin", database="keruneg")

        if self.conn.is_connected():
            print("Connected to MySQL Workbench!")

        # Buat atribut cursor di dalam objek Keruneg
        self.cursor = self.conn.cursor()

        self.root = root
        self.root.title(
            "SISTEM INFORMASI PIUTANG JANGKA PANJANG LAINNYA")
        self.root.geometry("1530x800+0+0")

        self.Ref = IntVar()
        self.IdSikad = StringVar()
        self.JenisTemuan = StringVar()
        self.Es1 = StringVar()
        self.Satker = StringVar()
        self.NamaPJ = StringVar()
        self.Nip = StringVar()
        self.Jab = StringVar()
        self.JenisKasus = StringVar()
        self.JenisKerugian = StringVar()
        self.Thn = StringVar()
        self.Dokumen = StringVar()
        self.TglDok = StringVar()
        self.Ket = StringVar()
        self.Status = StringVar()
        self.Dok = StringVar()
        self.Total = IntVar()
        self.Ang = IntVar()
        self.Phs = IntVar()
        self.Sisa = IntVar()

        lbltitle = Label(self.root, bd=20, relief=RIDGE, text="SISTEM INFORMASI PIUTANG JANGKA PANJANG LAINNYA",
                         fg="red", bg="white", font=("times new roman", 30, "bold"))
        lbltitle.pack(side=TOP, fill=X)

        # ==================== Data Frame ================
        DataFrame = Frame(self.root, bd=10, relief=RIDGE)
        DataFrame.place(x=0, y=100, width=1350, height=385)

        DataFrameLeft = LabelFrame(DataFrame, bd=5, padx=10, relief=RIDGE,
                                   font=("arial", 12, "bold"), text="Informasi Piutang")
        DataFrameLeft.place(x=5, y=5, width=1320, height=350)

        # ======================= Button Frame ==============
        ButtonFrame = Frame(self.root, bd=10, relief=RIDGE)
        ButtonFrame.place(x=0, y=490, width=1350, height=60)

        # ======================= Details Frame ==============
        Detailsframe = Frame(self.root, bd=10, relief=RIDGE)
        Detailsframe.place(x=0, y=545, width=1350, height=135)

        # ======================= DataFrame 2 ==============
        lblRef = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Reference No:",  padx=2, pady=4)
        lblRef.grid(row=0, column=0, sticky=W)
        txtRef = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                       textvariable=self.Ref, width=50)
        txtRef.grid(row=0, column=1)

        lblIdSikad = Label(DataFrameLeft, font=("arial", 12, "bold"),
                           text="ID SIKAD :",  padx=2, pady=4)
        lblIdSikad.grid(row=1, column=0, sticky=W)
        txtIdSikad = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                           textvariable=self.IdSikad, width=50)
        txtIdSikad.grid(row=1, column=1)

        lblJenisTemuan = Label(DataFrameLeft, font=("arial", 12, "bold"),
                               text="Jenis Temuan :",  padx=2, pady=4)
        lblJenisTemuan.grid(row=2, column=0, sticky=W)
        comJenisTemuan = ttk.Combobox(
            DataFrameLeft, textvariable=self.JenisTemuan, state="readonly", font=("arial", 12, "bold"), width=48,)
        comJenisTemuan['value'] = (
            "BPK (Eksternal)", "Itjen (Internal)")
        comJenisTemuan.grid(row=2, column=1)

        lblEs1 = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Eselon 1 :",  padx=2, pady=4)
        lblEs1.grid(row=3, column=0, sticky=W)
        txtEs1 = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                       textvariable=self.Es1, width=50)
        txtEs1.grid(row=3, column=1)

        lblSatker = Label(DataFrameLeft, font=("arial", 12, "bold"),
                          text="Satuan Kerja :",  padx=2, pady=4)
        lblSatker.grid(row=4, column=0, sticky=W)
        txtSatker = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                          textvariable=self.Satker, width=50)
        txtSatker.grid(row=4, column=1)

        lblNamaPJ = Label(DataFrameLeft, font=("arial", 12, "bold"),
                          text="Nama Penanggung Jawab :",  padx=2, pady=4)
        lblNamaPJ.grid(row=5, column=0, sticky=W)
        txtNamaPJ = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                          textvariable=self.NamaPJ, width=50)
        txtNamaPJ.grid(row=5, column=1)

        lblNip = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="NIP PJ :",  padx=2, pady=4)
        lblNip.grid(row=6, column=0, sticky=W)
        txtNip = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                       textvariable=self.Nip, width=50)
        txtNip.grid(row=6, column=1)

        lblJab = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Jabatan PJ :",  padx=2, pady=4)
        lblJab.grid(row=7, column=0, sticky=W)
        txtJab = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                       textvariable=self.Jab, width=50)
        txtJab.grid(row=7, column=1)

        lblJenisKasus = Label(DataFrameLeft, font=("arial", 12, "bold"),
                              text="Jenis Kasus :",  padx=2, pady=4)
        lblJenisKasus.grid(row=8, column=0, sticky=W)
        txtJenisKasus = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                              textvariable=self.JenisKasus, width=50)
        txtJenisKasus.grid(row=8, column=1)

        lblJenisKerugian = Label(DataFrameLeft, font=("arial", 12, "bold"),
                                 text="Jenis Kerugian :",  padx=2, pady=4)
        lblJenisKerugian.grid(row=9, column=0, sticky=W)
        comJenisKerugian = ttk.Combobox(
            DataFrameLeft, textvariable=self.JenisKerugian, state="readonly", font=("arial", 12, "bold"), width=48,)
        comJenisKerugian['value'] = (
            "TP", "TGR", "PIII")
        comJenisKerugian.grid(row=9, column=1)

        lblThn = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Tahun Kejadian :",  padx=2, pady=4)
        lblThn.grid(row=0, column=2, sticky=W)
        txtThn = Entry(DataFrameLeft, font=("arial", 13, "bold"),
                       textvariable=self.Thn, width=50)
        txtThn.grid(row=0, column=3)

        lblDokumen = Label(DataFrameLeft, font=("arial", 12, "bold"),
                           text="Dokumen LHP/A :",  padx=2, pady=4)
        lblDokumen.grid(row=1, column=2, sticky=W)
        txtDokumen = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.Dokumen,  width=50)
        txtDokumen.grid(row=1, column=3)

        lblTglDok = Label(DataFrameLeft, font=("arial", 12, "bold"),
                          text="Tanggal Dokumen :",  padx=2, pady=4)
        lblTglDok.grid(row=2, column=2, sticky=W)
        txtTglDok = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.TglDok,  width=50)
        txtTglDok.grid(row=2, column=3)

        lblKet = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Keterangan :",  padx=2, pady=4)
        lblKet.grid(row=3, column=2, sticky=W)
        txtKet = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.Ket,  width=50)
        txtKet.grid(row=3, column=3)

        lblStatus = Label(DataFrameLeft, font=("arial", 12, "bold"),
                          text="Status :",  padx=2, pady=4)
        lblStatus.grid(row=4, column=2, sticky=W)
        comStatus = ttk.Combobox(
            DataFrameLeft, textvariable=self.Status, state="readonly", font=("arial", 12, "bold"), width=48,)
        comStatus['value'] = (
            "Informasi", "Penetapan", "Tuntas", "TATD", "TPTD", "Penghapusan")
        comStatus.grid(row=4, column=3)

        lblDok = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Dokumen :", padx=2, pady=4)
        lblDok.grid(row=5, column=2, sticky=W)
        txtDok = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.Dok,  width=42)
        txtDok.grid(row=5, column=3, sticky=W)
        btnDok = Button(DataFrameLeft, text="Browse",
                        command=self.browse_file)
        btnDok.grid(row=5, column=3, sticky=E, padx=(0, 10))

        lblTotal = Label(DataFrameLeft, font=("arial", 12, "bold"),
                         text="Total Nilai :",  padx=2, pady=4)
        lblTotal.grid(row=6, column=2, sticky=W)
        txtTotal = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.Total,  width=50)
        txtTotal.grid(row=6, column=3)

        lblAng = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Nilai Angsuran :",  padx=2, pady=4)
        lblAng.grid(row=7, column=2, sticky=W)
        txtAng = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.Ang,  width=50)
        txtAng.grid(row=7, column=3)

        lblPhs = Label(DataFrameLeft, font=("arial", 12, "bold"),
                       text="Nilai Penghapusan :",  padx=2, pady=4)
        lblPhs.grid(row=8, column=2, sticky=W)
        txtPhs = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.Phs,  width=50)
        txtPhs.grid(row=8, column=3)

        lblSisa = Label(DataFrameLeft, font=("arial", 12, "bold"),
                        text="Sisa Angsuran :",  padx=2, pady=4)
        lblSisa.grid(row=9, column=2, sticky=W)
        txtSisa = Entry(DataFrameLeft, font=(
            "arial", 13, "bold"), textvariable=self.Sisa,  width=50)
        txtSisa.grid(row=9, column=3)

        # ======================= Buttons ==================
        btnTambah = Button(ButtonFrame, text="Tambah", bg="green", fg="white", font=(
            "arial", 12, "bold"), width=16, padx=12, pady=6, command=self.Tambah)
        btnTambah.grid(row=0, column=0)

        btnEdit = Button(ButtonFrame, text="Edit", bg="green", fg="white", font=(
            "arial", 12, "bold"), width=16, padx=12, pady=6, command=self.Edit)
        btnEdit.grid(row=0, column=1)

        btnHapus = Button(ButtonFrame, text="Hapus", bg="green", fg="white", font=(
            "arial", 12, "bold"), width=16, padx=12, pady=6, command=self.Hapus)
        btnHapus.grid(row=0, column=2)

        btnCari = Button(ButtonFrame, text="Cari", bg="green", fg="white", font=(
            "arial", 12, "bold"), width=16, padx=12, pady=6, command=self.Cari)
        btnCari.grid(row=0, column=3)

        btnClear = Button(ButtonFrame, text="Clear", bg="green", fg="white", font=(
            "arial", 12, "bold"), width=15, padx=12, pady=6, command=self.Clear)
        btnClear.grid(row=0, column=4)

        btnInfo = Button(ButtonFrame, text="Info", bg="green", fg="white", font=(
            "arial", 12, "bold"), width=16, padx=12, pady=6, command=self.show_info)
        btnInfo.grid(row=0, column=5)

        btnKeluar = Button(ButtonFrame, text="Keluar", bg="green", fg="white", font=(
            "arial", 12, "bold"), width=15, padx=12, pady=6, command=root.destroy)
        btnKeluar.grid(row=0, column=6)

        # ======================= Table ==================
        # ======================= ScrollBar ==================

        scroll_x = ttk.Scrollbar(Detailsframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Detailsframe, orient=VERTICAL)
        self.keruneg_table = ttk.Treeview(
            Detailsframe,
            columns=("Ref", "IdSikad", "JenisTemuan", "Es1", "Satker", "NamaPJ", "JenisKasus",
                     "JenisKerugian", "Thn", "Dokumen", "Ket", "Status", "Total", "Ang", "Phs", "Sisa"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Menetapkan command ke xview dan yview
        self.keruneg_table.configure(
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        self.keruneg_table.heading("Ref", text="Ref")
        self.keruneg_table.heading("IdSikad", text="ID")
        self.keruneg_table.heading("JenisTemuan", text="JT")
        self.keruneg_table.heading("Es1", text="Es1")
        self.keruneg_table.heading("Satker", text="Satker")
        self.keruneg_table.heading("NamaPJ", text="PJ")
        self.keruneg_table.heading("JenisKasus", text="JKas")
        self.keruneg_table.heading("JenisKerugian", text="JKer")
        self.keruneg_table.heading("Thn", text="Th")
        self.keruneg_table.heading("Dokumen", text="LHP/LHA")
        self.keruneg_table.heading("Ket", text="Ket")
        self.keruneg_table.heading("Status", text="Status")
        self.keruneg_table.heading("Total", text="Total Nilai")
        self.keruneg_table.heading("Ang", text="Angsuran")
        self.keruneg_table.heading("Phs", text="Penghapusan")
        self.keruneg_table.heading("Sisa", text="Sisa")

        self.keruneg_table["show"] = "headings"

        self.keruneg_table.column("Ref", width=25)
        self.keruneg_table.column("IdSikad", width=50)
        self.keruneg_table.column("JenisTemuan", width=30)
        self.keruneg_table.column("Es1", width=75)
        self.keruneg_table.column("Satker", width=100)
        self.keruneg_table.column("NamaPJ", width=30)
        self.keruneg_table.column("JenisKasus", width=200)
        self.keruneg_table.column("JenisKerugian", width=50)
        self.keruneg_table.column("Thn", width=50)
        self.keruneg_table.column("Dokumen", width=80)
        self.keruneg_table.column("Ket", width=50)
        self.keruneg_table.column("Status", width=80)
        self.keruneg_table.column("Total", width=100)
        self.keruneg_table.column("Ang", width=100)
        self.keruneg_table.column("Phs", width=100)
        self.keruneg_table.column("Sisa", width=100)

        self.keruneg_table.pack(fill=BOTH, expand=1)

        # ======================= Functionality Declaration ==================

    # def show_info(self):
    #     from info import Info
    #     if not self.root.winfo_exists():  # Pengecekan keberadaan jendela utama
    #         return

    #     self.info = Info(self.root)
    #     # Menutup aplikasi keruneg.py saat info.py dipanggil
    #     self.root.destroy()
    def show_info(self):
        from info import Info

        def close_root():
            if self.root.winfo_exists():
                self.root.destroy()

        if not self.root.winfo_exists():
            return

        self.info = Info(self.root)
        # Menutup aplikasi keruneg.py setelah jendela info.py ditampilkan
        self.root.after(100, close_root)

    def RefreshTable(self):
        try:
            with self.conn.cursor() as cursor:
                # Query untuk mengambil semua data dari tabel temuan dan keuangan dengan join
                query_join = """
                    SELECT t.ref, t.id_sikad, t.jenis_temuan, t.es1, t.satker, t.nama_pj,
                        t.jenis_kasus, t.jenis_kerugian, t.thn, t.dokumen, t.ket, t.status,k.total, k.ang, k.phs, k.sisa
                    FROM temuan t
                    LEFT JOIN keuangan k ON t.ref = k.ref
                """
                cursor.execute(query_join)
                rows = cursor.fetchall()

                # Hapus semua item di Treeview sebelum menambahkan yang baru
                for item in self.keruneg_table.get_children():
                    self.keruneg_table.delete(item)

                # Menambahkan data hasil join ke Treeview
                for row in rows:
                    self.keruneg_table.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat memuat data. Silakan coba lagi. Error: {str(e)}")

    def Tambah(self):
        try:
            with self.conn.cursor() as cursor:
                # Mengambil data dari input langsung
                values_temuan = (
                    self.Ref.get(),
                    self.IdSikad.get(),
                    self.JenisTemuan.get(),
                    self.Es1.get(),
                    self.Satker.get(),
                    self.NamaPJ.get(),
                    self.Nip.get(),
                    self.Jab.get(),
                    self.JenisKasus.get(),
                    self.JenisKerugian.get(),
                    self.Thn.get(),
                    self.Dokumen.get(),
                    self.TglDok.get(),
                    self.Ket.get(),
                    self.Status.get(),
                    self.Dok.get(),
                )

                # Format tanggal
                try:
                    tgl_dok = datetime.strptime(
                        self.TglDok.get(), "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror(
                        "Error", "Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
                    return

                # Masukkan data ke tabel temuan
                query_temuan = """
                    INSERT INTO temuan (
                        ref, id_sikad, jenis_temuan, es1, satker, nama_pj, nip, jab, jenis_kasus,
                        jenis_kerugian, thn, dokumen, tgl_dok, ket, status, dok
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_temuan, values_temuan)

                # Setelah query temuan dijalankan, kita bisa mendapatkan nilai dari ref untuk digunakan dalam query ke tabel keuangan
                ref_keuangan = self.Ref.get()

                # Masukkan data ke tabel keuangan
                query_keuangan = """
                    INSERT INTO keuangan (ref, total, ang, phs, sisa)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values_keuangan = (
                    ref_keuangan,
                    self.Total.get(),
                    self.Ang.get(),
                    self.Phs.get(),
                    # Hitung sisa sebagai selisih total dengan ang dan phs
                    int(self.Total.get()) - \
                    int(self.Ang.get()) - int(self.Phs.get()),
                )

                cursor.execute(query_keuangan, values_keuangan)

                # Commit perubahan ke database
                self.conn.commit()

                messagebox.showinfo("Sukses", "Data berhasil disimpan!")

                # Setelah data berhasil disimpan, kosongkan inputan
                self.Clear()
                self.RefreshTable()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat memproses data. Silakan coba lagi. Error: {str(e)}")

    def Cari(self):
        try:
            with self.conn.cursor() as cursor:
                # Ambil nilai dari inputan Reference Number atau Id Sikad
                ref_cari = self.Ref.get()
                id_sikad_cari = self.IdSikad.get()

                # Query untuk mencari data berdasarkan Reference Number atau Id Sikad
                query_cari = """
                    SELECT * FROM temuan
                    WHERE ref = %s OR id_sikad = %s
                """
                cursor.execute(query_cari, (ref_cari, id_sikad_cari))
                data = cursor.fetchone()

                if data:
                    # Jika data ditemukan, isi nilai kolom lainnya sesuai dengan data yang ditemukan
                    self.Ref.set(data[0])
                    self.IdSikad.set(data[1])
                    self.JenisTemuan.set(data[2])
                    self.Es1.set(data[3])
                    self.Satker.set(data[4])
                    self.NamaPJ.set(data[5])
                    self.Nip.set(data[6])
                    self.Jab.set(data[7])
                    self.JenisKasus.set(data[8])
                    self.JenisKerugian.set(data[9])
                    self.Thn.set(data[10])
                    self.Dokumen.set(data[11])
                    self.TglDok.set(data[12])
                    self.Ket.set(data[13])
                    self.Status.set(data[14])
                    self.Dok.set(data[15])

                    # Query untuk mencari data di tabel keuangan
                    query_keuangan = """
                        SELECT * FROM keuangan
                        WHERE ref = %s
                    """
                    cursor.execute(query_keuangan, (ref_cari,))
                    data_keuangan = cursor.fetchone()

                    if data_keuangan:
                        # Jika data keuangan ditemukan, isi nilai kolom Total, Ang, Phs, dan Sisa
                        self.Total.set(data_keuangan[1])
                        self.Ang.set(data_keuangan[2])
                        self.Phs.set(data_keuangan[3])
                        self.Sisa.set(data_keuangan[4])

                    messagebox.showinfo("Sukses", "Data ditemukan!")

                else:
                    messagebox.showinfo("Informasi", "Data tidak ditemukan!")

        except Exception as e:
            messagebox.showerror(
                "Error", "Terjadi kesalahan saat mencari data. Silakan coba lagi.")

    def Edit(self):
        try:
            with self.conn.cursor() as cursor:
                # Ambil nilai dari inputan Reference Number
                ref_edit = self.Ref.get()

                # Query untuk mengupdate data temuan
                query_edit_temuan = """
                    UPDATE temuan
                    SET id_sikad=%s, jenis_temuan=%s, es1=%s, satker=%s, nama_pj=%s,
                        nip=%s, jab=%s, jenis_kasus=%s, jenis_kerugian=%s, thn=%s,
                        dokumen=%s, tgl_dok=%s, ket=%s, status=%s, dok=%s
                    WHERE ref=%s
                """
                values_edit_temuan = (
                    self.IdSikad.get(),
                    self.JenisTemuan.get(),
                    self.Es1.get(),
                    self.Satker.get(),
                    self.NamaPJ.get(),
                    self.Nip.get(),
                    self.Jab.get(),
                    self.JenisKasus.get(),
                    self.JenisKerugian.get(),
                    self.Thn.get(),
                    self.Dokumen.get(),
                    self.TglDok.get(),
                    self.Ket.get(),
                    self.Status.get(),
                    self.Dok.get(),
                    ref_edit,
                )
                cursor.execute(query_edit_temuan, values_edit_temuan)

                # Query untuk mengupdate data keuangan
                query_edit_keuangan = """
                    UPDATE keuangan
                    SET total=%s, ang=%s, phs=%s, sisa=%s
                    WHERE ref=%s
                """
                values_edit_keuangan = (
                    self.Total.get(),
                    self.Ang.get(),
                    self.Phs.get(),
                    # Hitung sisa sebagai selisih total dengan ang dan phs
                    int(self.Total.get()) - \
                    int(self.Ang.get()) - int(self.Phs.get()),
                    ref_edit,
                )
                cursor.execute(query_edit_keuangan, values_edit_keuangan)

                # Commit perubahan ke database
                self.conn.commit()

                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")

                # Clear the text fields after a successful edit
                self.Clear()
                self.RefreshTable()

        except Exception as e:
            messagebox.showerror(
                "Error", "Terjadi kesalahan saat mengedit data. Silakan coba lagi.")

    def Hapus(self):
        try:
            with self.conn.cursor() as cursor:
                # Ambil nilai dari inputan Reference Number atau Id Sikad
                ref_hapus = self.Ref.get()

                # Query untuk menghapus data keuangan
                query_hapus_keuangan = """
                    DELETE FROM keuangan
                    WHERE ref = %s
                """
                cursor.execute(query_hapus_keuangan, (ref_hapus,))

                # Query untuk menghapus data temuan
                query_hapus_temuan = """
                    DELETE FROM temuan
                    WHERE ref = %s
                """
                cursor.execute(query_hapus_temuan, (ref_hapus,))

                # Commit perubahan ke database
                self.conn.commit()

                messagebox.showinfo("Sukses", "Data berhasil dihapus!")

                # Setelah data berhasil dihapus, kosongkan inputan
                self.Clear()
                self.RefreshTable()

        except Exception as e:
            messagebox.showerror(
                "Error", "Terjadi kesalahan saat menghapus data. Silakan coba lagi.")

    def Clear(self):
        # Clear the text fields
        self.Ref.set("")
        self.IdSikad.set("")
        self.JenisTemuan.set("")
        self.Es1.set("")
        self.Satker.set("")
        self.NamaPJ.set("")
        self.Nip.set("")
        self.Jab.set("")
        self.JenisKasus.set("")
        self.JenisKerugian.set("")
        self.Thn.set("")
        self.Dokumen.set("")
        self.TglDok.set("")
        self.Ket.set("")
        self.Status.set("")
        self.Dok.set("")
        self.Total.set(0)
        self.Ang.set(0)
        self.Phs.set(0)
        self.Sisa.set(0)


try:
    root = tk.Tk()
    ob = MainApp(root)
    ob.RefreshTable()
    root.mainloop()

finally:
    # Close the database connection when the Tkinter window is closed
    if ob.conn.is_connected():
        ob.conn.close()
        print("MySQL Connection Closed.")
