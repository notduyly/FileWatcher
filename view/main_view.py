import tkinter as tk

class FileWatcherGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_window()

    def setup_window(self):
        self.root.title("File System Watcher")
        self.root.geometry("500x500")

        self.start_button = tk.Button(
            self.root,
            text="Start",
            font=('Arial', 20),
            command=self.start_watching
        )
        self.start_button.pack(padx=10, pady=10)

        self.stop_button = tk.Button(
            self.root,
            text="Stop",
            font=('Arial', 20),
            command=self.stop_watching
        )
        self.stop_button.pack(padx=10, pady=20)

    def start_watching(self):
        self.controller.start_watching() 

    def stop_watching(self):
        self.controller.stop_watching()


