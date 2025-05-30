import sys
import os
import tkinter as tk

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from model.db_handler import (
    query_events, 
    export_to_csv as db_export_to_csv,
    reset_database as db_reset
)
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
        try:
            if hasattr(self, '__query_window') and self.__query_window is not None:
                self.__query_window.focus()
            else:
                self.__query_window = QueryWindow(self.__myView.get_root(), self)
                self.__query_window.grab_set()
        except tk.TclError:
            self.__query_window = QueryWindow(self.__myView.get_root(), self)
            self.__query_window.grab_set()

    def get_filtered_events(self, filters):
        """Get filtered events from database"""
        return query_events(filters)

    def export_to_csv(self, file_path, events):
        """Export events to CSV file"""
        try:
            return db_export_to_csv(file_path, events)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def reset_database(self):
        """Reset the database"""
        try:
            return db_reset()
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False

    def send_email_results(self, recipient, file_path):
        """Send email with results"""
        try:
            # Code for sending email
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def get_available_extensions(self):
        """Get list of available file extensions"""
        from model.db_handler import get_unique_extensions
        return get_unique_extensions()