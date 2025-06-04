import tkinter as tk

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from model.db_handler import (
    query_events,
    reset_database as db_reset
)
from view.query_window import QueryWindow
from tkinter import filedialog
from model.email_sender import send_email_with_attachment

class WatcherController:
    def __init__(self):
        self.__myWatcher = None
        self.__myView = None
        self.__myWatchDirectory = ''
        self.__myFileExtension = ''

    def set_view(self, theView):
        self.__myView = theView

    def get_view(self):
        return self.__myView

    def start_watching(self):
        if not self.__myWatchDirectory:
            print("No directory selected to watch.")
            return
        
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

    def get_filtered_events(self, theFilters):
        return query_events(theFilters)

    def reset_database(self):
        try:
            return db_reset()
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False

    def send_email_results(self, recipient, thePath):
        return send_email_with_attachment(recipient, thePath)

    def get_available_extensions(self):
        from model.db_handler import get_unique_extensions
        return get_unique_extensions()

    def save_events_to_database(self, theEvents):
        from model.db_handler import save_multiple_events
        return save_multiple_events(theEvents)

    def format_event(self, theEvent):
        from model.db_handler import format_event_for_display
        return format_event_for_display(theEvent)

    def validate_email(self, theEmail):
        from model.email_sender import validate_email
        return validate_email(theEmail)

    def export_to_csv(self, thePath, theEvents):
        from model.db_handler import export_events_to_csv
        return export_events_to_csv(thePath, theEvents)
