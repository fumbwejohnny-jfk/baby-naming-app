
import tkinter as tk
import csv
from itertools import islice
from tkinter import filedialog, messagebox
from functools import partial

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

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
        # tk.Button(self, text="Logout", command=lambda: controller.show_frame(LoginPage)).pack()

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


       