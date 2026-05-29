import tkinter as tk
from BabyNameClient import BabyNameClient
from tkinter import messagebox
import requests
from AdminPage import  AdminPage
from UserPage import UserPage

BASE_URL = "http://localhost:8000/api/v1/"  # Replace with your actual base URL

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        
        # parent.title("Baby Name Application - Login")
        # self.geometry("400x250")
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
        req = {
            # "command": "LOGIN",
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        resp = requests.post(BASE_URL + "auth/login/", json=req).json()
        print(f"Login response: {self.client.username} — {resp}")  # Debug print to check response structure

        if resp.get('detail'):
            messagebox.showerror("Login Failed", resp['detail'])
            return
      
        self.client.getUserInfo(resp)  # Fetch user info after login to determine role
        
        if self.client.username is not None:
            self.destroy()
            if self.client.role == 'Admin':
                self.controller.show_frame(AdminPage)
            else:
                self.controller.show_frame(UserPage)
        else:
            messagebox.showerror("Login Failed",  resp.get('message', 'Try again!'))