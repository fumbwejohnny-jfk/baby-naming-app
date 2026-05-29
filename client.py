import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://localhost:8000/api/v1/"

access_token = None


# LOGIN FUNCTION
def login():

    global access_token

    username = username_entry.get()
    password = password_entry.get()

    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(
            f"{BASE_URL}auth/login/",
            json=data
        )

        if response.status_code == 200:

            tokens = response.json()

            access_token = tokens["access"]

            messagebox.showinfo(
                "Success",
                "Login successful"
            )

            load_tasks()

        else:
            messagebox.showerror(
                "Error",
                "Invalid credentials"
            )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# LOAD TASKS
def load_tasks():

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:

        response = requests.get(
            f"{BASE_URL}tasks/",
            headers=headers
        )

        if response.status_code == 200:

            tasks = response.json().get("results", [])
            print(tasks)

            task_listbox.delete(0, tk.END)

            for task in tasks:

                task_text = (
                    f"{task['title']} "
                    f"({task['status']})"
                )

                task_listbox.insert(
                    tk.END,
                    task_text
                )

        else:
            messagebox.showerror(
                "Error",
                "Failed to load tasks"
            )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# TKINTER UI
root = tk.Tk()
root.title("Task Manager")
root.geometry("500x500")


# USERNAME
tk.Label(root, text="Username").pack()

username_entry = tk.Entry(root)
username_entry.pack()


# PASSWORD
tk.Label(root, text="Password").pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()


# LOGIN BUTTON
login_button = tk.Button(
    root,
    text="Login",
    command=login
)

login_button.pack(pady=10)


# TASK LIST
task_listbox = tk.Listbox(
    root,
    width=60,
    height=20
)

task_listbox.pack(pady=20)


root.mainloop()