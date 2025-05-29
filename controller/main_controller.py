import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from view.query_window import QueryWindow
from tkinter import filedialog

class WatcherController:
    def __init__(self):
        self.__myWatcher = None
        self.__myView = None
        self.__myWatchDirectory = ''
        self.__myFileExtension = ''

    def set_view(self, theView):
        self.__myView = theView

    def start_watching(self):
        handler = MyEventHandler(logToTextbox=self.__myView.add_log)

        if self.__myFileExtension and self.__myFileExtension != 'None':
            handler.set_extension_filter(self.__myFileExtension)

        self.__myWatcher = FileWatcher(self.__myWatchDirectory, handler)
        self.__myWatcher.start()
        print(f"Started watching directory: {self.__myWatchDirectory}")
    
    def stop_watching(self):
        if self.__myWatcher:
            self.__myWatcher.stop()
            print("Stopped watching")

    def open_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.__myWatchDirectory = directory
            self.__myView.update_directory_display(directory)
            print(f"Selected directory: {directory}")
    
    def set_file_extension(self, theExtension):
        self.__myFileExtension = theExtension
        print(f"Selected extension filter: {theExtension}")
        print(self.__myWatchDirectory)
        
    def open_query_window(self):
        """Open database query window"""
        if hasattr(self, 'query_window') and self.__query_window is not None:
            try:
                self.__query_window.focus()
            except tk.TclError:
                self.__query_window = QueryWindow(self.__myView.get_root(), self)
        else:
            self.__query_window = QueryWindow(self.__myView.get_root(), self)
