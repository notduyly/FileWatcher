import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from tkinter import filedialog, messagebox

class WatcherController:
    def __init__(self):
        self.myWatcher = None
        self.myView = None
        self.myWatchDirectory = ''
        self.myFileExtension = ''

    def set_view(self, view):
        self.myView = view

    def start_watching(self):
        handler = MyEventHandler(logToTextbox=self.myView.add_log)

        if self.myFileExtension and self.myFileExtension != 'None':
            handler.set_extension_filter(self.myFileExtension)

        self.myWatcher = FileWatcher(self.myWatchDirectory, handler)
        self.myWatcher.start()
        print(f"Started watching directory: {self.myWatchDirectory}")
    
    def stop_watching(self):
        if self.myWatcher:
            self.myWatcher.stop()
            print("Stopped watching")

    def open_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.myWatchDirectory = directory
            self.myView.update_directory_display(directory)
            print(f"Selected directory: {directory}")
    
    def set_file_extension(self, theExtension):
        self.myFileExtension = theExtension
        print(f"Selected extension filter: {theExtension}")
        print(self.myWatchDirectory)