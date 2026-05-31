import tkinter as tk
from pages.LoginPage import LoginPage
from pages.UserPage import UserPage



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Baby Name Application")
        # self.geometry("400x300")

        # main container
        self.container = tk.Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack(fill="both", expand=True)

        # dictionary to hold different frames
        self.frames = {}

        # initialize all frames and store in the dictionary
        for F in (LoginPage,  UserPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # start with the login page
        self.show_frame(LoginPage)


    """Function to raise the specified frame to the top for display."""
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()