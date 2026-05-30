import tkinter as tk
from LoginPage import LoginPage
from UserPage import UserPage
from AdminPage import AdminPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Baby Name Application - Main")
        # self.geometry("400x300")

        # main container
        self.container = tk.Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (LoginPage, AdminPage, UserPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()