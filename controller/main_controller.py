import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from view.query_window import QueryWindow
from tkinter import filedialog

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
        else:
            self.query_window = QueryWindow(self.myView.myRoot, self)

    def query_events(self, query_type="all", **kwargs):
        """Query events from database through db_handler"""
        from model.db_handler import fetch_all_events, fetch_event_by_extension, fetch_event_by_after_date, fetch_event_by_type;
        
        try:
            if query_type == "By Extension":
                extension = kwargs.get('extension', 'All')
                return fetch_event_by_extension(extension)
            
            elif query_type == "By Event Type":
                event_type = kwargs.get('event_type', 'All')
                return fetch_event_by_type(event_type)
                
            elif query_type == "By Date":
                date_range = kwargs.get('date_range', 'All')
                return fetch_event_by_after_date(date_range)
                
            else:
                return fetch_all_events()
                
        except Exception as e:
            print(f"Error querying events: {e}")
            return []

    def reset_database(self):
        """Reset database through db_handler"""
        from model.db_handler import reset_database
        
        try:
            return reset_database()
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
