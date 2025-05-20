import sys
import os
import csv

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from model.db_handler import (fetch_all_events, fetch_event_by_type,
                            fetch_event_by_extension, fetch_event_by_after_date)
from tkinter import filedialog
# from model.email_sender import EmailSender

class WatcherController:
    def __init__(self):
        self.watcher = None
        self.view = None
        self.watch_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "testFileToWatch")

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
            print(f"Selected directory: {directory}")

    def query_events(self, extension=None, start_date=None):
        """Query events from database based on filters"""
        if start_date:
            results = fetch_event_by_after_date(start_date)
        else:
            results = fetch_all_events()
            
        if extension and extension != "All":
            results = [r for r in results if r[2] == extension]
            
        return results
    
    def export_to_csv(self, file_path: str, data: list) -> bool:
        """Export data to CSV file"""
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Extension", "Filename", "PATH", "Event", "Date/Time"])
                for row in data:
                    writer.writerow(row)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
            
    def send_email_results(self, recipient: str, attachment_path: str) -> bool:
        """Send email with query results"""
        try:
            sender = EmailSender(sender_email="your@email.com", 
                               password="your_app_password")
            return sender.send_email_with_attachment(
                recipient_email=recipient,
                subject="File Watcher Query Result",
                body="Please find the attached CSV file of the query result.",
                attachment_path=attachment_path
            )
        except Exception as e:
            print(f"Email error: {e}")
            return False