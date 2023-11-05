import logging
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from directories import DB_DIR, LOGS_DIR, REPORT_DIR, BRAND_DIR, ICONS_DIR, DB_DIR
from tkinter import messagebox, Menu
import webbrowser
from usermanagement import UserManager 
from tkinter import ttk, messagebox
from tkinter import ttk, PhotoImage
from help_file import HelpWindow
# Setting up logging
logging.basicConfig(filename='dashboard.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

BRAND_DIR = os.path.join(BRAND_DIR, "Company_logo.png")

class Welcome_Login:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to IoTShield")
        self.master.geometry("800x500")
        self.master.config(bg="#6941C7")

        # Configuring style for transparent background
        style = ttk.Style()
        style.configure("TLabel", background="#6941C7")
        style.configure("TEntry", fieldbackground="#6941C7")
        style.configure("TButton", background="#6941C7")

        # Welcome message
        self.label_welcome = ttk.Label(self.master, text="Welcome to IoTShield", font=("Microsoft JhengHei UI", 24), foreground="white")
        self.label_welcome.place(x=200, y=50)

        # Logo (replace 'placeholder.png' with your logo path)
        self.logo = PhotoImage(file="company_logo.png")
        self.logo_label = ttk.Label(self.master, image=self.logo, background="#6941C7")
        self.logo_label.place(x=300, y=100)

        # Login name
        self.label_name = ttk.Label(self.master, text="Login Name:", font=("Microsoft JhengHei UI", 12), foreground="white")
        self.label_name.place(x=250, y=280)
        self.entry_name = ttk.Entry(self.master, font=("Microsoft JhengHei UI", 12))
        self.entry_name.place(x=350, y=280)

        # Password
        self.label_password = ttk.Label(self.master, text="Password:", font=("Microsoft JhengHei UI", 12), foreground="white")
        self.label_password.place(x=250, y=320)
        self.entry_password = ttk.Entry(self.master, show="*", font=("Microsoft JhengHei UI", 12))
        self.entry_password.place(x=350, y=320)

        # "Remember Me" Checkbox
        self.remember_var = tk.IntVar()
        self.checkbox_remember = ttk.Checkbutton(self.master, text="Remember Me", variable=self.remember_var)
        self.checkbox_remember.place(x=350, y=360)

        # Login button
        self.btn_login = ttk.Button(self.master, text="Login", command=self.login)
        self.btn_login.place(x=350, y=400)

        # Link to website (replace '#' with your website link)
        self.link_website = ttk.Label(self.master, text="Visit our website", cursor="hand2", font=("Microsoft JhengHei UI", 12), foreground="white")
        self.link_website.place(x=320, y=450)
        self.link_website.bind("<Button-1>", lambda e: self.open_web("#"))

    def open_web(self, link):
        import webbrowser
        webbrowser.open_new(link)

    def login(self):
        user = self.entry_name.get()
        password = self.entry_password.get()
        if UserManager().validate_user(user, password):
            print("Logged in successfully")
        else:
            print("Invalid credentials!")

    def create_widgets(self):
        # Welcome message
        self.welcome_label = tk.Label(self.master, text="Welcome to IoTShield™", font=("Microsoft JhengHei UI", 16, "bold"))
        self.welcome_label.pack(pady=20)

        # Logo
        self.logo = tk.PhotoImage(file="company_logo.png")
        self.logo_label = tk.Label(self.master, image=self.logo)
        self.logo_label.pack(pady=20)

        # Login frame
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack(pady=20)

        # Username
        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Microsoft JhengHei UI", 12))
        self.username_label.pack(row=0, column=0, padx=10, sticky="e")
        self.username_entry = tk.Entry(self.login_frame, font=("Microsoft JhengHei UI", 12))
        self.username_entry.pack(row=0, column=1, padx=10)

        # Password
        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Microsoft JhengHei UI", 12))
        self.password_label.pack(row=1, column=0, padx=10, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, font=("Microsoft JhengHei UI", 12), show="*")
        self.password_entry.pack(row=1, column=1, padx=10)

        # Buttons
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=20)

        self.login_button = tk.Button(self.buttons_frame, text="Login", font=("Microsoft JhengHei UI", 12, "bold"), command=self.login)
        self.login_button.pack(row=0, column=0, padx=10)

        self.help_button = tk.Button(self.buttons_frame, text="Help", font=("Microsoft JhengHei UI", 12, "bold"), command=self.open_help)
        self.help_button.pack(row=0, column=1, padx=10)

        self.exit_button = tk.Button(self.buttons_frame, text="Exit", font=("Microsoft JhengHei UI", 12, "bold"), command=self.exit_program)
        self.exit_button.pack(row=0, column=2, padx=10)

        # Link to website
        self.website_label = tk.Label(self.master, text="Visit our website", font=("Microsoft JhengHei UI", 12, "underline"), fg="blue", cursor="hand2")
        self.website_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://aicybersolutions.eu/"))
        self.website_label.pack(pady=20)

class User:
    def __init__(self, username, password, access_level):
        self.username = username
        self.password = password
        self.access_level = access_level

    def can_view(self):
        return self.access_level in ["view", "view_print", "full"]

    def can_print(self):
        return self.access_level in ["view_print", "full"]

    def has_full_access(self):
        return self.access_level == "full"

class UserManager:
    def __init__(self):
        self.users = {
            "Admin": User("Admin", "Admin1234&&", "full"),
            "Emma": User("Emma", "ViewPrint1234&&", "view_print"),
            "Andy": User("Andy", "View1234&&", "view")
        }

    def authenticate(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
            user = self.user_manager.authenticate(username, password)
            
            if user:
                self.parent.user = user
                self.pack_forget()  # Hide the login frame
                self.parent.show_dashboard_content()  # Show main dashboard content
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except Exception as e:
            logging.error("Error in authentication: " + str(e))
            messagebox.showerror("Error", "An unexpected error occurred. Please check the log for details.")

    def view_content(user):
        if user.can_view():
            return "You are viewing the content."
        return "You don't have permission to view the content."

    def print_content(user):
        if user.can_print():
            return "You are printing the content."
        return "You don't have permission to print the content."

    def modify_content(user):
        if user.has_full_access():
            return "You have modified the content."
        return "You don't have permission to modify the content."



if __name__ == "__main__":
    root = tk.Tk()
    app = Welcome_Login(root)
    root.mainloop()