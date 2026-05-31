# from LoginPage import LoginPage
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BabyNameClient import BabyNameClient
from library.baby_library import convert_json_to_babies, search_baby_meaning
from library.baby_stats_library import convert_json_to_babies_stats, search_baby_name


class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.client = BabyNameClient()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self)
        content.grid(row=0, column=0, sticky="nsew")
       

         # All data table
        tk.Label(content, text="All Baby Names with their meanings", font=("Arial", 20)).pack(pady=5)
        self.tree = ttk.Treeview(content, columns=("name", "meaning"), show="headings")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("meaning", width=400, anchor="w")
        self.tree.heading("name", text="Name")
        self.tree.heading("meaning", text="Meaning")
        self.tree.pack( padx=10, pady=5)
        tk.Button(content, text="Refresh Names List", command=self.load_all_names).pack(ipady=10)

        # Search section
        search_section = tk.Frame(content)
        search_frame = tk.Frame(search_section)
        search_frame.grid(row=0, column=0, pady=10)
        search_frame.pack(pady=20)
        tk.Label(search_frame, text="Search by Name", font=("Arial", 13)).grid(row=0, column=0, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 14))
        self.search_entry.grid(row=0, column=1, padx=5, ipady=3)

        btn_frame = tk.Frame(search_section)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Show Meaning", command=self.show_meaning).pack(side="left", ipady=10, padx=5)
        tk.Button(btn_frame, text="Show Usage Charts", command=self.show_charts).pack(side="left", ipady=10, padx=5)
        btn_frame.grid(row=0, column=1, pady=10)
        search_section.pack()

        # Result area
        self.meaning_label = tk.Label(content, text="Meaning will be displayed here", wraplength=800, font=("Arial", 12),
                                      justify="left", bg="#f0f0f0", bd=2, relief="groove", padx=10, pady=10)
        self.meaning_label.pack(pady=10)

        self.chart_frame = tk.Frame(content, bg="white", width=1000, height=400)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20,ipadx=10, ipady=10)

        # logout button
        # tk.Button(content, text="Logout", command=lambda: controller.show_frame(LoginPage)).pack()
        self.load_all_names()

    """Load all babies from local JSON file and display in the treeview."""
    def load_all_names(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
       
        babies = convert_json_to_babies("names/babies.json")
        self.client.babies = babies  # Store babies in client for later use in search
       
        if babies:
            for baby in babies:
                self.tree.insert("", "end", values=(baby.name, baby.meaning))

    """Show meaning of the searched name. Placeholder response is used here"""
    def show_meaning(self):
        name = self.search_entry.get().strip()
        if not name:
            return
        resp = {"status": "failed", "meaning": ""}  # Placeholder response
        
        meaning = search_baby_meaning(self.client.babies, name)
        resp = {"status": "success", "meaning": meaning} if meaning else resp
        self.meaning_label.config(
            text=f"{resp.get('meaning', 'Not found')}" if resp['status'] == 'success' else "Error")

    """Show usage charts for the searched name. Placeholder response is used here."""
    def show_charts(self):
        name = self.search_entry.get().strip()
        if not name or search_baby_meaning(self.client.babies, name) is None:
            return
        resp = {"status": "failed", "usage": []}  # Placeholder response

        if not self.client.babies_stats:
            stats = convert_json_to_babies_stats("names/stats.json")
            self.client.babies_stats = stats  # Store stats in client for later use in search
        data = search_baby_name(self.client.babies_stats, name)
        resp = {"status": "success", "usage": data} if data else resp
        if resp['status'] != 'success' or not resp['usage']:
            messagebox.showinfo("No Data", "No usage data found for this name.")
            return

        usage = resp['usage']
        # Functional grouping
        male_data = list(filter(lambda x: x.gender == 'M', usage))
        female_data = list(filter(lambda x: x.gender == 'F', usage))

        years_m = [int(d.yob) for d in male_data]
        counts_m = [int(d.ranking) for d in male_data]

        years_f = [int(d.yob) for d in female_data]
        counts_f = [int(d.ranking) for d in female_data]

        total_m = sum(counts_m)
        total_f = sum(counts_f)

        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
       # BarChart
        bar_width = 0.8

        if years_m:
            ax1.bar(
            np.array(years_m) - bar_width / 2,
            counts_m,
            width=bar_width,
            label='Male',
            color='blue'
        )

        if years_f:
            ax1.bar(
                np.array(years_f) + bar_width / 2,
                counts_f,
                width=bar_width,
                label='Female',
                color='orange'
            )
            ax1.set_title(f'Usage of "{name}" Over Years')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Count')
            ax1.legend()
            ax1.grid(False)

            # PieChart
            if total_m + total_f > 0:
                ax2.pie([total_m, total_f], labels=['Male', 'Female'], autopct='%1.1f%%', colors=['blue', 'orange'])
                ax2.set_title('Gender Distribution')
            else:
                ax2.text(0.5, 0.5, 'No data', ha='center')
        
        # Prevent overlapping of subplots
        fig.tight_layout()

        # Embed the matplotlib figure in Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # important
        self.canvas = canvas  # Keep reference to prevent garbage collection
        plt.close(fig)  # Close the figure to free memory

        # tk.Button(
        #     self,
        #     text="Logout",
        #     # command=lambda: controller.show_frame(LoginPage)
        # ).pack()