import datetime
import tkinter as tk
from logging import root
from tkinter import ttk

import matplotlib.pyplot as plt
import pytz
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class IoTShieldDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set title and size
        self.title("IoT Shield Dashboard")
        self.geometry("1500x900")

        # Set background color
        self.configure(bg="#6941C7")

        # Create left sidebar frame
        self.left_sidebar_frame = tk.Frame(self, bg="#6941C7", width=250,
                                           height=800)
        self.left_sidebar_frame.pack_propagate(0)
        self.left_sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Example: Create a digital clock for London in the left sidebar
        self.create_clock("London")

        self.main_frame = tk.Frame(self, bg="#6941C7")
        self.main_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        # Create a style object for ttk
        style = ttk.Style()
        style.configure('TButton', font=("Microsoft JhengHei UI", 12))

        # Logo
        self.logo_image = tk.PhotoImage(file="company_logo.png")
        logo_label = tk.Label(self.left_sidebar_frame, image=self.logo_image,
                              bg="#6941C7", font=("Microsoft JhengHei UI", 12))
        logo_label.pack(pady=20)

        # Clocks
        self.create_clock("London")
        self.create_clock("Paris")
        self.create_clock("New York")

        # Buttons (from IoTShield_GUI.py)
        self.bg_color = "#6941C7"
        self.button_frame = tk.Frame(self.left_sidebar_frame, bg=self.bg_color)
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        module_paths = ["Module 1", "Module 2", "Module 3", "Module 4"]
        max_width = max([len(m) for m in module_paths])

        for module_path in module_paths:
            btn = ttk.Button(self.button_frame, text=module_path,
                             width=max_width, command=self.open_module)
            btn.pack(fill=tk.BOTH, padx=10, pady=5)

        website_btn = ttk.Button(self.button_frame, text="Visit Website",
                                 command=self.open_website)
        website_btn.pack(fill=tk.BOTH, padx=10, pady=5)

    def create_clock(self, timezone):
        city_label = tk.Label(self.left_sidebar_frame, text=timezone,
                              font=("Microsoft JhengHei UI", 12, "bold"),
                              bg="#6941C7", fg="white")
        city_label.pack(pady=5)
        time_label = tk.Label(self.left_sidebar_frame, text="",
                              font=("Microsoft JhengHei UI", 16), bg="#6941C7",
                              fg="white")
        time_label.pack(pady=10)

        def update_time():
            if self._root():
                current_time = datetime.datetime.now(pytz.timezone
                                                     (city_timezones[timezone]
                                                      )).strftime('%H:%M:%S')
                time_label.config(text=current_time)
                time_label.after(1000, update_time)

        update_time()

    def create_main_content(self):
        # Sample graph using matplotlib
        figure, ax = plt.subplots(figsize=(4, 3), dpi=100)
        figure.patch.set_facecolor('#6941C7')

        sample_data = [1, 4, 2, 5, 2, 5, 3, 6, 2, 1, 1]
        ax.plot(sample_data, color='#d8c3f8')
        ax.set_facecolor('#bb8fce')
        ax.set_title('Sample Graph', color='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        canvas = FigureCanvasTkAgg(figure, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def open_module(self):
        print("Opening module...")

    def open_website(self):
        print("Opening website...")


if __name__ == "__main__":
    city_timezones = {
        "London": "Europe/London",
        "Paris": "Europe/Paris",
        "New York": "America/New_York"
    }
    dashboard = IoTShieldDashboard()
    dashboard.mainloop()
    root.geometry("1500x900")  # Set an initial size for the window
