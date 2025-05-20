import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from tkinter import filedialog, messagebox

class WatcherController:
    def __init__(self):
        self.watcher = None
        self.view = None
        self.watch_directory = None

    def set_view(self, view):
        self.view = view

    def start_watching(self):
        for file in self.watch_directory:
            handler = MyEventHandler(logToTextbox=self.view.add_log)
            self.watcher = FileWatcher(file, handler)
            self.watcher.start()
            print(f"Started watching directory: {self.watch_directory}")
    
    def stop_watching(self):
        if self.watcher:
            self.watcher.stop()
            print("Stopped watching")

    def open_directory(self):
        choice = messagebox.askyesno("Selection Type", 
                                    "Would you like to select a file?\n\nYes = Select File\nNo = Select Directory")

        if choice:  # User wants to select a file
            directory = filedialog.askopenfilenames(title="Select File to Watch")
            self.watch_directory = list(directory)
        else:  # User wants to select a directory
            directory = filedialog.askdirectory(title="Select Directory to Watch")
            self.watch_directory = [directory]