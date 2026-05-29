import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import socket
import json
import csv
from itertools import islice
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
import requests

from client import load_tasks

from client import load_tasks

BASE_URL = "http://localhost:8000/api/v1/"
access_token = None

class BabyNameClient:
    def __init__(self):
        self.sock = None
        # self.role = None
        # self.build_login_window()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("127.0.0.1", 5555))

    def send_request(self, request):
        self.sock.sendall(json.dumps(request).encode("utf-8"))
        resp = self.sock.recv(8192).decode("utf-8")
        return json.loads(resp)

    def build_login_window(self):
        self.root = tk.Tk()
        self.root.title("Baby Name Application - Login")
        # Username, Password entries + Login button
        # On successful login → self.show_main_window()
        # ... (standard Tkinter grid layout)

    def show_main_window(self):
        # Clear login window
        if self.role == "admin":
            self.build_admin_ui()
        else:
            self.build_user_ui()

    def build_admin_ui(self):
        # Buttons: "Upload Baby Names & Meanings (CSV/TXT)", "Upload End-Users (CSV/TXT)"
        # Multiple file selection allowed
        upload_names_btn = tk.Button(..., command=self.upload_names)
        # upload_names: filedialog.askopenfilenames(), read CSV/TXT with csv.reader or functional map, send {"command":"UPLOAD_NAMES", "data": list_of_tuples}



    def build_user_ui(self):
        # Left: Treeview (all data)
        self.tree = ttk.Treeview(..., columns=("name", "meaning"))
        tk.Button(text="Load All Names", command=self.load_all_names).pack()

        # Search sections
        tk.Label(text="Enter Baby Name:").pack()
        self.name_entry = tk.Entry()
        self.name_entry.pack()

        tk.Button(text="Show Meaning", command=self.show_meaning).pack()
        tk.Button(text="Show Usage Charts", command=self.show_charts).pack()

        # Frame for charts
        self.chart_frame = tk.Frame()
        self.chart_frame.pack()

    def load_all_names(self):
        resp = self.send({"command": "GET_ALL_NAMES"})
        # Populate Treeview (functional: for row in resp["data"])

    def show_meaning(self):
        name = self.name_entry.get().strip()
        resp = self.send({"command": "GET_MEANING", "name": name})
        messagebox.showinfo("Meaning", resp["meaning"])

    def show_charts(self):
        name = self.name_entry.get().strip()
        resp = self.send({"command": "GET_STATS", "name": name})
        stats = resp["stats"]  # {'F': [(year, rank), ...], 'M': [...]}

        # Clear previous charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Functional style to prepare data
        fig = plt.Figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Line Chart: usage (rank) over years per gender
        for gender, data in stats.items():
            years, ranks = zip(*data) if data else ([], [])
            ax1.plot(years, ranks, label=gender, marker='o')
        ax1.set_title(f"Usage Trend for '{name}'")
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Rank (lower = more popular)")
        ax1.legend()

        # Pie Chart: gender distribution (total entries per gender)
        gender_counts = {g: len(d) for g, d in stats.items()}
        if gender_counts:
            ax2.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%')
            ax2.set_title("Gender Distribution")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baby Name Application - Login")
        self.geometry("400x250")
        self.client = BabyNameClient()
        # self.client.connect()

        # username
        tk.Label(self, text="Baby Name ", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # password
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        #button
        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    # Process login
    def login(self):
      
        username = self.username_entry.get()
        password = self.password_entry.get()    
        data = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post( f"{BASE_URL}auth/login/", json=data )
       

            if response.status_code == 200:
                tokens = response.json()
                access_token = tokens["access"]
                messagebox.showinfo( "Success", "Login successful" )

                # load_tasks()

            else:
                messagebox.showerror( "Error", "Invalid credentials")

        except Exception as e:
            messagebox.showerror("Error",  str(e)   )
        
        print(f"Response: {access_token}")
        if resp['status']== 'success':
            self.destroy()
            if resp['role'] == 'admin':
                AdminWindow(self.client)
            else:
                UserWindow(self.client)
        else:
            messagebox.showerror("Login Failed",  resp.get('message', 'Try again!'))


class AdminWindow(tk.Toplevel):
    def __init__(self, client):
        super().__init__()
        self.title("Admin Panel")
        self.geometry("500x400")
        self.client = client

        #
        tk.Label(self, text="Administrator Controls", font=("Arial", 14)).pack(pady=10)

        #button
        # Buttons: "Upload Baby Names & Meanings (CSV/TXT)", "Upload End-Users (CSV/TXT)"
        # Multiple file selection allowed
        tk.Button(self, text="Upload Baby Names & Meanings (CSV /TXT",
                                     command=partial(self.upload_csv, 'UPLOAD_NAMES', ['name', 'meaning'])).pack(pady=10)
        # upload_names: filedialog.askopenfilenames(), read CSV/TXT with csv.reader o

        tk.Button(self, text="Upload Usage Data (CSV)",
                  command=partial(self.upload_csv, 'upload_usage', ['name', 'year', 'gender', 'count'])).pack(pady=5)
        tk.Button(self, text="Upload End-Users (CSV)",
                  command=partial(self.upload_csv, 'upload_users', ['username', 'password', 'role'])).pack(pady=5)

        tk.Button(self, text="Logout", command=self.destroy).pack(pady=20)

    # upload baby names and meaning from files
    def upload_names(self, command, expected_keys):
        # Allow selection of multiple text files
        file_paths = filedialog.askopenfilenames(
            title="Select one or more text/csv files",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.*")]
        )

        if not file_paths:
            return  # User cancelled

        file_list = list(file_paths)  # tuple → list

        # Show confirmation with example
        example = " | ".join(expected_keys)
        msg = (f"Selected {len(file_list)} text file(s):\n\n" +
               "\n".join([f"• {f.split('/')[-1]}" for f in file_list[:5]]) +  # show first 5
               ("\n   ... and more" if len(file_list) > 5 else "") +
               f"\n\nExpected format per line:\n{example}\n\n"
               f"Example: John | God is gracious\n\n"
               f"Proceed with uploading all lines from these files?")

        if not messagebox.askyesno("Confirm Multi-File Upload", msg):
            return

        req = {
            'command': command,
            'file_paths': file_list   # Send list of paths to server
        }

        resp = self.client.send_request(req)

        if resp['status'] == 'success':
            messagebox.showinfo("Upload Successful", resp['message'])
        else:
            messagebox.showerror("Upload Failed", resp.get('message', 'Unknown error'))

    def upload_csv(self, command, expected_keys):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            data = [row for row in reader if all(k in row for k in expected_keys)]
        if not data:
            messagebox.showerror("Error", "Invalid CSV format")
            return
        data = list(islice(data, 2000))

        # Create a new list containing only the allowed keys
        cleaned_data = [
            {"name": item["name"], "meaning": item["meaning"]}
            for item in data
        ]

        # send data in a chunk of 10 rows
        chunk_size = 10
        size = len(cleaned_data)
        total_count = 0
        for i in range(0, size, chunk_size):
            # Extract 10 rows
            chunk = cleaned_data[i: i + chunk_size]

            # Send the chunk
            # req = {'command': 'append_data', 'data': chunk}
            # resp = self.client.send_request(req)
            req = {'command': command, 'data': chunk}
            total_count += len(chunk)
            print(f"Sent {total_count} chunks to server...")
            resp = self.client.send_request(req)

            # update 10 rows sent
            print(f"Uploaded data: {resp['message']}")
        #messagebox.showinfo("Upload", resp.get('message', 'Done'))

    def upload_users(self, command, expected_keys):
        pass


class UserWindow(tk.Toplevel):
    def __init__(self, client):
        super().__init__()
        self.title("Baby Name Explorer")
        self.geometry("900x700")
        self.client = client

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

        self.load_all_names()

    def load_all_names(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        resp = self.client.send_request({'command': 'GET_ALL_NAMES'})
        print(f"All Names: {resp}")
        if resp['status'] == 'success':
            for row in resp['data']:
                self.tree.insert("", "end", values=(row['name'], row['meaning']))

    def show_meaning(self):
        name = self.search_entry.get().strip()
        if not name:
            return
        resp = self.client.send_request({'command': 'GET_MEANING', 'name': name})
        self.meaning_label.config(
            text=f"Meaning: {resp.get('meaning', 'Not found')}" if resp['status'] == 'success' else "Error")

    def show_charts(self):
        name = self.search_entry.get().strip()
        if not name:
            return
        resp = self.client.send_request({'command': 'GET_USAGE', 'name': name})
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


if __name__ == "__main__":
    # Create ./data/ folder and place your yob1880.txt ... yob2023.txt files before running server
    # client = BabyNameClient()
    # client.root.mainloop()
    LoginWindow().mainloop()
