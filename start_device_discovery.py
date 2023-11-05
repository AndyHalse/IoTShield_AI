    def start_device_discovery(self):
        ip_range = self.ip_range_input.text()
        if not ip_range:
            QMessageBox.warning(self, "Input Error", "Please enter an IP range (e.g., 192.168.1.1/24).")
            return

        self.scanner = NetworkScanner(ip_range)
        self.scanner.progressUpdate.connect(self.update_progress)
        self.scanner.scan()

        self.progress_bar.setRange(0, 0)
        self.statusBar().showMessage("Scanning in progress...")
        self.log_to_terminal("Start Scanning...")