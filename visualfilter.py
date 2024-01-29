import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualfilter:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=560, height=170)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_y = ttk.Scrollbar(
            self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.scrollbar_x = ttk.Scrollbar(
            self.master, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(
            yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.content_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(
            (0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.grid_columnconfigure(0, weight=1)

        self.es1_filter_combobox = ttk.Combobox(
            self.content_frame, width=15, state="readonly")
        self.es1_filter_combobox.grid(row=0, column=1, padx=5, sticky="w")

        self.es1_filter_label = ttk.Label(
            self.content_frame, text="Filter Es1:", anchor="e", width=15)
        self.es1_filter_label.grid(row=0, column=0, padx=5, sticky="e")

        self.create_sunburst_chart()

        self.update_button = ttk.Button(
            self.content_frame, text="Update Chart", command=self.update_chart)
        self.update_button.grid(row=1, column=0, pady=10)

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.update_chart()

    def create_sunburst_chart(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin",
                database="keruneg"
            )
            query = "SELECT * FROM temuan"
            data = pd.read_sql_query(query, conn)
            conn.close()

            es1_values = [""] + data['es1'].unique().tolist()
            self.es1_filter_combobox['values'] = es1_values
            self.es1_filter_combobox.set("--Pilih Eselon 1--")

            def filter_data_by_es1(*args):
                selected_es1 = self.es1_filter_combobox.get()
                filtered_data = data[data['es1'] == selected_es1]
                self.plot_pie_chart(filtered_data)

            self.es1_filter_combobox.bind(
                "<<ComboboxSelected>>", filter_data_by_es1)
            self.plot_pie_chart(data)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def plot_pie_chart(self, data):
        grouped_data_level1 = data.groupby(
            'jenis_temuan').size().reset_index(name='jumlah_level1')
        grouped_data_level2 = data.groupby(
            ['jenis_temuan', 'jenis_kerugian']).size().reset_index(name='jumlah_level2')

        sorted_data_level1 = self.quick_sort(
            grouped_data_level1, 'jenis_temuan')
        sorted_data_level2 = self.quick_sort(
            grouped_data_level2, 'jenis_temuan')

        fig, ax = plt.subplots(figsize=(5, 5))
        colors_level1 = plt.cm.Dark2(
            range(len(sorted_data_level1['jenis_temuan'])))
        colors_level2 = plt.cm.Paired(
            range(len(sorted_data_level2['jenis_kerugian'])))

        labels_level2 = sorted_data_level2['jenis_temuan'] + \
            ' - ' + sorted_data_level2['jenis_kerugian']
        wedges_level2, _, _ = ax.pie(
            sorted_data_level2['jumlah_level2'],
            labels=None,
            startangle=90,
            colors=colors_level2,
            autopct='',
            textprops=dict(color="w")
        )

        for wedge, label, value in zip(wedges_level2, labels_level2, sorted_data_level2['jumlah_level2']):
            angle = (wedge.theta2 + wedge.theta1) / 2.
            x = 0.80 * np.sin(np.deg2rad(angle))
            y = 0.80 * np.cos(np.deg2rad(angle))
            ax.text(x, y, f"{label}\n{value:.0f}", ha='center',
                    va='center', fontsize=6, color='black', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.5'))

        labels_level1 = sorted_data_level1['jenis_temuan']
        wedges_level1, _, _ = ax.pie(
            sorted_data_level1['jumlah_level1'],
            labels=None,
            startangle=90,
            colors=colors_level1,
            radius=0.75,
            textprops=dict(color="w"),
            autopct=''
        )

        for wedge, label, value in zip(wedges_level1, labels_level1, sorted_data_level1['jumlah_level1']):
            angle = (wedge.theta2 + wedge.theta1) / 2.
            x = 0.5 * np.sin(np.deg2rad(angle))
            y = 0.5 * np.cos(np.deg2rad(angle))
            ax.text(x, y, f"{label}\n{value:.0f}", ha='center',
                    va='center', fontsize=6, color='black', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.5'))
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0)

    def quick_sort(self, data, col):
        if len(data) <= 1:
            return data
        else:
            pivot = data[col].iloc[0]
            lesser = data[data[col] < pivot]
            equal = data[data[col] == pivot]
            greater = data[data[col] > pivot]
            return pd.concat([self.quick_sort(lesser, col), equal, self.quick_sort(greater, col)], ignore_index=True)

    def update_chart(self):
        self.create_sunburst_chart()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = tk.Tk()
    app = Visualfilter(root)
    root.mainloop()
