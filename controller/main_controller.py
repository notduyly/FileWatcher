import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from tkinter import filedialog, messagebox

class WatcherController:
    def __init__(self):
        self.watcher = None
        self.view = None
        self.watch_directory = ''

    def set_view(self, view):
        self.view = view

    def start_watching(self):
        if self.watcher:
            print("Already watching.")
            return
            
        handler = MyEventHandler(logToTextbox=self.view.add_log)
        self.watcher = FileWatcher(self.watch_directory[0], handler)
        self.watcher.start()
        print(f"Started watching directory: {self.watch_directory[0]}")
    
    def stop_watching(self):
        if self.watcher:
            self.watcher.stop()
            self.watcher = None
            print("Stopped watching")

    def open_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            if self.watcher:
                self.stop_watching()
                
            self.watch_directory = [directory]
            self.start_watching()