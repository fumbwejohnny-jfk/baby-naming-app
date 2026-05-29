# from LoginPage import LoginPage
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
       

         # All data table
        tk.Label(self, text="All Baby Names", font=("Arial", 12)).pack(pady=5)
        self.tree = ttk.Treeview(self, columns=("name", "meaning"), show="headings", height=8)
        self.tree.heading("name", text="Name")
        self.tree.heading("meaning", text="Meaning")
        self.tree.pack(fill="x", padx=10)
        tk.Button(self, text="Refresh Names List", command=self.load_all_names).pack(pady=5)

        # Search section
        tk.Label(self, text="Search by Name", font=("Arial", 12)).pack(pady=(20, 5))
        self.search_entry = tk.Entry(self, width=30)
        self.search_entry.pack()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Show Meaning", command=self.show_meaning).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Show Usage Charts", command=self.show_charts).pack(side="left", padx=5)

        # Result area
        self.meaning_label = tk.Label(self, text="", wraplength=800, justify="left")
        self.meaning_label.pack(pady=10)

        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # logout button
        tk.Button(self, text="Logout", command=lambda: controller.show_frame(LoginPage)).pack()

        # self.load_all_names()

    def load_all_names(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        resp = {"status": "failed", "data": []}  # Placeholder response'}
        # self.client.send_request({'command': 'GET_ALL_NAMES'})
        print(f"All Names: {resp}")
        if resp['status'] == 'success':
            for row in resp['data']:
                self.tree.insert("", "end", values=(row['name'], row['meaning']))

    def show_meaning(self):
        name = self.search_entry.get().strip()
        if not name:
            return
        resp = {"status": "failed", "meaning": ""}  # Placeholder response
        #self.client.send_request({'command': 'GET_MEANING', 'name': name})
        self.meaning_label.config(
            text=f"Meaning: {resp.get('meaning', 'Not found')}" if resp['status'] == 'success' else "Error")

    def show_charts(self):
        name = self.search_entry.get().strip()
        if not name:
            return
        resp = {"status": "failed", "usage": []}  # Placeholder response
        #self.client.send_request({'command': 'GET_USAGE', 'name': name})
        if resp['status'] != 'success' or not resp['usage']:
            messagebox.showinfo("No Data", "No usage data found for this name.")
            return

        usage = resp['usage']
        # Functional grouping
        male_data = list(filter(lambda x: x['gender'] == 'M', usage))
        female_data = list(filter(lambda x: x['gender'] == 'F', usage))

        years_m = [d['year'] for d in male_data]
        counts_m = [d['count'] for d in male_data]
        years_f = [d['year'] for d in female_data]
        counts_f = [d['count'] for d in female_data]

        total_m = sum(counts_m)
        total_f = sum(counts_f)

        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        # LineChart
        if years_m:
            ax1.plot(years_m, counts_m, marker='o', label='Male', color='blue')
        if years_f:
            ax1.plot(years_f, counts_f, marker='o', label='Female', color='pink')
        ax1.set_title(f'Usage of "{name}" Over Years')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Count')
        ax1.legend()
        ax1.grid(True)

        # PieChart
        if total_m + total_f > 0:
            ax2.pie([total_m, total_f], labels=['Male', 'Female'], autopct='%1.1f%%', colors=['blue', 'pink'])
            ax2.set_title('Gender Distribution')
        else:
            ax2.text(0.5, 0.5, 'No data', ha='center')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Button(
            self,
            text="Logout",
            # command=lambda: controller.show_frame(LoginPage)
        ).pack()