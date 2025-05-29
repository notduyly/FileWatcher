import sys
import os
import tkinter as tk
from tkinter import filedialog

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from view.query_window import QueryWindow

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
        
    def open_query_window(self):
        """Open database query window"""
        if hasattr(self, 'query_window') and self.query_window is not None:
            try:
                self.query_window.focus()
            except tk.TclError:
                self.query_window = QueryWindow(self.myView.myRoot, self)
                self.query_window.grab_set()
        else:
            self.query_window = QueryWindow(self.myView.myRoot, self)
            self.query_window.grab_set()

    def query_events(self, filters=None):
        """Forward query request to db_handler"""
        from model.db_handler import query_events
        return query_events(filters)

    def reset_database(self):
        """Reset database through db_handler"""
        from model.db_handler import reset_database
        try:
            success = reset_database()
            if success:
                print("Database reset successfully")
            else:
                print("Failed to reset database")
            return success
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False

    def export_to_csv(self, file_path, results):
        """Export results to CSV through db_handler"""
        from model.db_handler import export_to_csv
        
        try:
            return export_to_csv(file_path, results)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
