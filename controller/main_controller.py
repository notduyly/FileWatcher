import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from tkinter import filedialog, messagebox
import tkinter as tk

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

    def open_query_window(self):
        """Open database query window"""
        from view.query_window import QueryWindow
        if hasattr(self, 'query_window') and self.query_window is not None:
            try:
                self.query_window.focus()
            except tk.TclError:
                self.query_window = QueryWindow(self.view.root, self)
        else:
            self.query_window = QueryWindow(self.view.root, self)