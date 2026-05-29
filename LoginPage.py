import tkinter as tk
from BabyNameClient import BabyNameClient
from tkinter import messagebox
from AdminPage import  AdminPage
from UserPage import UserPage

admin = {"username": "Admin", "password": "admin123"}
user = {"username": "User", "password": "user123"}

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

    """This module contains functions to process login request and response."""
    def process_login(self, req):
        username = req["username"]
        password = req["password"]
        resp = None
        if username == admin["username"] and password == admin["password"]:
            resp = {"user": {"username": admin["username"], "is_admin": True}}
        elif username == user["username"] and password == user["password"]:
            resp = {"user": {"username": user["username"], "is_admin": False}}
        else:
            resp = {"detail": "Invalid username or password"}
        return resp
    
    
    # Process login
    def login(self):
        req = {
            # "command": "LOGIN",
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        resp = self.process_login(req)
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