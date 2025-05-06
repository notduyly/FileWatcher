import tkinter as tk
import sys
import os

class FileWatcherGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.controller.set_view(self)
        self.setup_window()

    def setup_window(self):
        self.root.title("File System Watcher")
        self.root.geometry("500x500")

        self.start_button = tk.Button(
            self.root,
            text="Start",
            font=('Arial', 20),
            command=self.controller.start_watching
        )
        self.start_button.pack(padx=10, pady=10)

        self.stop_button = tk.Button(
            self.root,
            text="Stop",
            font=('Arial', 20),
            command=self.controller.stop_watching
        )
        self.stop_button.pack(padx=10, pady=20)

        self.log_text = tk.Text(self.root, state='disabled', wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)

    def add_log(self, message: str):
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')


