import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from tkinter import filedialog

class WatcherController:
    def __init__(self):
        self.watcher = None
        self.view = None
        self.watch_directory = ''

    def set_view(self, view):
        self.view = view

    def start_watching(self):
        handler = MyEventHandler(logToTextbox=self.view.add_log)
        self.watcher = FileWatcher(self.watch_directory, handler)
        self.watcher.start()
        print(f"Started watching directory: {self.watch_directory}")
    
    def stop_watching(self):
        if self.watcher:
            self.watcher.stop()
            print("Stopped watching")

    def open_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.watch_directory = directory
            print(f"Selected directory: {directory}")