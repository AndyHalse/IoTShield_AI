import tkinter as tk
from tkinter import ttk, Text, Scrollbar
import webbrowser

class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.callbacks = {}

    def add(self, action):
        tag = "hyper-%d" % len(self.callbacks)
        self.callbacks[tag] = action
        return tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                self.callbacks[tag]()
                return

class HelpWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.title("Help")
        self.geometry("800x600")

        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text = Text(self.frame, wrap="word", yscrollcommand=self.scrollbar.set)
        self.text.pack(expand=True, fill="both")

        self.scrollbar.config(command=self.text.yview)

        self.text.insert("end", self.get_help_content())
        self.text.config(state="disabled")

        self.hyperlink = HyperlinkManager(self.text)
        self.text.tag_configure("h1", font=("Microsoft JhengHei UI", 12, "bold"))
        self.text.tag_configure("normal", font=("Microsoft JhengHei UI", 12))
        self.text.tag_configure("italic", font=("Microsoft JhengHei UI", 12, "italic"))

        self.text.tag_bind(self.hyperlink.add(lambda: webbrowser.open("https://aicybersolutions.eu/")), "<Button-1>")
        
        self.search_label = ttk.Label(self.frame, text="Search:")
        self.search_label.pack(side="left", padx=5)
        
        self.search_entry = ttk.Entry(self.frame)
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.search_button = ttk.Button(self.frame, text="Search", command=self.search_content)
        self.search_button.pack(side="left", padx=5)
        
        self.exit_button = ttk.Button(self.frame, text="Close", command=self.destroy)
        self.exit_button.pack(side="right", padx=5)

    def search_content(self):
        search_term = self.search_entry.get()
        if not search_term:
            return
        
        start = "1.0"
        while True:
            start = self.text.search(search_term, start, stopindex=tk.END)
            if not start:
                break
            end = f"{start} + {len(search_term)}c"
            self.text.tag_add("search", start, end)
            start = end
        self.text.tag_config("search", background="yellow")

    def get_help_content(self):
        # Your actual help content goes here.
        # For demonstration purposes, I'll return a dummy string.
        return """Your Help Content Here..."""

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    HelpWindow(root)
    root.mainloop()
