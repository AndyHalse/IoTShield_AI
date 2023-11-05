import tkinter as tk
from cefpython3 import cefpython as cef

class DeviceApp:
    # ... existing methods ...

    def create_main_display(self):
        # ... existing code ...

        # Create a frame for the browser
        self.browser_frame = tk.Frame(self)
        self.browser_frame.pack(fill=tk.BOTH, expand=tk.YES)

        # Embed the Chromium browser
        self.embed_browser()

    def embed_browser(self):
        window_info = cef.WindowInfo(self.browser_frame.winfo_id())
        cef.Initialize()
        self.browser = cef.CreateBrowserSync(url="https://aicybersolutions.eu/", window_info=window_info)
        self.browser.SetClientHandler(LoadHandler())

        # Set focus on the browser
        self.browser_frame.focus_set()

        # Start the cefpython message loop (this will keep the browser active and responsive)
        cef.MessageLoop()

class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        # Handle loading state change, if needed
        pass

# ... rest of the script ...

