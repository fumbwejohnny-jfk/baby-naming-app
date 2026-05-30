import tkinter as tk
from BabyNameClient import BabyNameClient
from tkinter import Label, messagebox
from AdminPage import  AdminPage
from UserPage import UserPage

admin = {"username": "Admin", "password": "admin123"}
user = {"username": "User", "password": "user123"}

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="#d9d9d9",
    bd=4,
    relief="solid",
    padx=50,
    pady=50)
        content.grid(row=0, column=0)        
        # parent.title("Baby Name Application - Login")
        # self.geometry("400x250")
        self.client = BabyNameClient()
        # self.client.connect()

        tk.Label(content, text="Baby Name ", font=("Arial", 30), fg="blue", bg="#d9d9d9").pack(pady=20)
        # username
        username_frame = tk.Frame(content)
        username_frame.pack(pady=5)
        tk.Label(username_frame, text="Username:", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
        self.username_entry= tk.Entry(username_frame, font=("Arial", 16))
        self.username_entry.grid(row=0, column=1, padx=5, ipady=5)
        username_frame.pack(pady=5)

        # password
        password_frame = tk.Frame(content)
        password_frame.pack(pady=5)
        tk.Label(password_frame, text="Password: ", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
        self.password_entry = tk.Entry(password_frame, show="*", font=("Arial", 16))
        self.password_entry.grid(row=0, column=1,ipady=5)
        password_frame.pack()

        #button
        tk.Button(content, text="Login", font=("Arial", 16), cursor="hand2", command=self.login).pack(pady=20, ipadx=10, ipady=5)
        

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
    
    
    """ This module contains functions to handle login logic, including validating credentials and navigating to the appropriate page based on user role."""
    def login(self):
        req = {
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        resp = self.process_login(req)
        # print(f"Login response: {self.client.username} — {resp}")  # Debug print to check response structure

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