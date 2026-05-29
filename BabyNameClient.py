import requests
import tkinter as tk

class BabyNameClient:
    def __init__(self):
        self.access_token = None
        self.role = None# Store JWT token after login for authenticated requests
        self.refresh_token = None
        self.username = None

    def getUserInfo(self, resp):
        self.access_token = resp.get("access")
        self.refresh_token = resp.get("refresh")
        user = resp.get("user")
        print(f"User info from response: {user}")  # Debug print to check user info structure
        self.username = user.get("username") if user else None  
        self.role = 'Admin' if user.get("is_admin") else 'User'
        
        
    # def get_user_info(self):
    #     if not self.access_token:
    #         return None
    #     headers = {"Authorization": f"Bearer {self.access_token}"}
    #     resp = requests.get(BASE_URL + "user_info/", headers=headers).json()
    #     if resp.status_code == 200:
    #         data = resp
    #         self.role =  'Admin' if data['is_admin'] else 'User'
    #         self.username = data['username']
            

    # def show_main_window(self):
    #     # Clear login window
    #     if self.role == "admin":
    #         self.build_admin_ui()
    #     else:
    #         self.build_user_ui()

    # def build_admin_ui(self):
    #     # Buttons: "Upload Baby Names & Meanings (CSV/TXT)", "Upload End-Users (CSV/TXT)"
    #     # Multiple file selection allowed
    #     upload_names_btn = tk.Button(..., command=self.upload_names)
    #     # upload_names: filedialog.askopenfilenames(), read CSV/TXT with csv.reader or functional map, send {"command":"UPLOAD_NAMES", "data": list_of_tuples}


    # def build_user_ui(self):
    #     # Left: Treeview (all data)
    #     self.tree = ttk.Treeview(..., columns=("name", "meaning"))
    #     tk.Button(text="Load All Names", command=self.load_all_names).pack()

    #     # Search sections
    #     tk.Label(text="Enter Baby Name:").pack()
    #     self.name_entry = tk.Entry()
    #     self.name_entry.pack()

    #     tk.Button(text="Show Meaning", command=self.show_meaning).pack()
    #     tk.Button(text="Show Usage Charts", command=self.show_charts).pack()

    #     # Frame for charts
    #     self.chart_frame = tk.Frame()
    #     self.chart_frame.pack()

    # def load_all_names(self):
    #     resp = self.send({"command": "GET_ALL_NAMES"})
    #     # Populate Treeview (functional: for row in resp["data"])

    # def show_meaning(self):
    #     name = self.name_entry.get().strip()
    #     resp = self.send({"command": "GET_MEANING", "name": name})
    #     messagebox.showinfo("Meaning", resp["meaning"])

    # def show_charts(self):
    #     name = self.name_entry.get().strip()
    #     resp = self.send({"command": "GET_STATS", "name": name})
    #     stats = resp["stats"]  # {'F': [(year, rank), ...], 'M': [...]}

    #     # Clear previous charts
    #     for widget in self.chart_frame.winfo_children():
    #         widget.destroy()

    #     # Functional style to prepare data
    #     fig = plt.Figure(figsize=(12, 5))
    #     ax1 = fig.add_subplot(121)
    #     ax2 = fig.add_subplot(122)

    #     # Line Chart: usage (rank) over years per gender
    #     for gender, data in stats.items():
    #         years, ranks = zip(*data) if data else ([], [])
    #         ax1.plot(years, ranks, label=gender, marker='o')
    #     ax1.set_title(f"Usage Trend for '{name}'")
    #     ax1.set_xlabel("Year")
    #     ax1.set_ylabel("Rank (lower = more popular)")
    #     ax1.legend()

    #     # Pie Chart: gender distribution (total entries per gender)
    #     gender_counts = {g: len(d) for g, d in stats.items()}
    #     if gender_counts:
    #         ax2.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%')
    #         ax2.set_title("Gender Distribution")

    #     canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
    #     canvas.draw()
    #     canvas.get_tk_widget().pack()
