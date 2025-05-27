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

    def query_events(self, filters=None):
        """Query events from database with combined filters"""
        from model.db_handler import get_connection
        
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM events WHERE 1=1"
                params = []
                
                if filters:
                    if filters['event_type'] != 'All':
                        query += " AND event = ?"
                        params.append(filters['event_type'])
                    
                    if filters['extension'] != 'All':
                        query += " AND file_extension = ?"
                        params.append(filters['extension'])
                    
                    if filters['date_range'] != 'All':
                        if filters['date_range'] == 'Today':
                            query += " AND DATE(event_timestamp) = DATE('now')"
                        elif filters['date_range'] == 'Last 7 days':
                            query += " AND event_timestamp >= datetime('now', '-7 days')"
                        elif filters['date_range'] == 'Last 30 days':
                            query += " AND event_timestamp >= datetime('now', '-30 days')"
                
                query += " ORDER BY event_timestamp DESC"
                print(f"Executing query: {query} with params: {params}")
                
                cursor.execute(query, params)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Database error: {e}")
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
