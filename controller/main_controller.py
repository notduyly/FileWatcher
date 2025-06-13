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
    """
    Controller class for managing file system watching operations.
    """
    
    def __init__(self):
        """Constructs the WatcherController"""
        self.__myWatcher = None
        self.__myView = None
        self.__myWatchDirectory = ''
        self.__myFileExtension = ''

    def set_view(self, theView):
        """
        Sets the view.

        Args:
            theView: The view object to associate with this controller.
        """
        self.__myView = theView

    def get_view(self):
        """
        Returns the current view component.

        Returns:
            The current view object associated with this controller.
        """
        return self.__myView

    def start_watching(self):
        """
        Creates a new FileWatcher instance with an event handler and begins
        monitoring the specified directory. Applies file extension filtering
        if chosen.
        """
        if not self.__myWatchDirectory:
            print("No directory selected to watch.")
            return
        
        handler = MyEventHandler(logToTextbox=self.__myView.add_log)

        if self.__myFileExtension and self.__myFileExtension != 'None':
            handler.set_extension_filter(self.__myFileExtension)

        self.__myWatcher = FileWatcher(self.__myWatchDirectory, handler)
        self.__myWatcher.start()
        
        # Disable the start button when watching begins
        self.__myView.get_window().set_start_button_state(False)
        
        print(f"Started watching directory: {self.__myWatchDirectory}")
    
    def stop_watching(self):
        """Stop the current file watching operation if one is active."""
        if self.__myWatcher:
            self.__myWatcher.stop()
            
            # Re-enable the start button when watching stops
            self.__myView.get_window().set_start_button_state(True)
            
            print("Stopped watching")

    def open_directory(self):
        """
        Opens a directory selection box and sets the watch directory.

        Also, updates the view to display the selected directory path.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.__myWatchDirectory = directory
            self.__myView.update_directory_display(directory)
            print(f"Selected directory: {directory}")
    
    def set_file_extension(self, theExtension):
        """
        Sets the file extension filter for monitoring.

        Args:
            theExtension (str): The file extension to filter for ('.txt', '.png', etc.).
        """
        self.__myFileExtension = theExtension
        print(f"Selected extension filter: {theExtension}")
        print(self.__myWatchDirectory)
        
    def open_query_window(self):
        """
        Open the database query window.
        
        Creates a new QueryWindow instance or focuses an existing one.
        Handles window management and ensures only one query window is open.
        """
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
        """
        Gets filtered events from the database.

        Args:
            theFilters: Filters for the query.

        Returns:
            List of events matching the specified filters.
        """
        return query_events(theFilters)

    def reset_database(self):
        """
        Resets the database.
        
        Returns:
            bool: True if reset was successful, False otherwise.
        """
        try:
            return db_reset()
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False

    def send_email_results(self, recipient, thePath):
        """
        Sends query results via email as an attachment.
        
        Args:
            recipient: Email address of the recipient.
            thePath: File path of the attachment to send.
            
        Returns:
            bool: True if email was sent successfully, False otherwise.
        """
        return send_email_with_attachment(recipient, thePath)

    def get_available_extensions(self):
        """
        Gets all unique file extensions from stored events.
        
        Returns:
            list: List of unique file extensions found in the database.
        """
        from model.db_handler import get_unique_extensions
        return get_unique_extensions()

    def save_events_to_database(self, theEvents):
        """
        Saves multiple events to the database.
        
        Args:
            theEvents: List of event objects to save.
            
        Returns:
            bool: True if events were saved successfully, False otherwise.
        """
        from model.db_handler import save_multiple_events
        return save_multiple_events(theEvents)

    def format_event(self, theEvent):
        """
        Format an event.
        
        Args:
            theEvent: Event object to format.
            
        Returns:
            str: Formatted string representation of the event.
        """
        from model.db_handler import format_event_for_display
        return format_event_for_display(theEvent)

    def validate_email(self, theEmail):
        """
        Validate an email address.
        
        Args:
            theEmail: Email address to validate.
            
        Returns:
            bool: True if email format is valid, False otherwise.
        """
        from model.email_sender import validate_email
        return validate_email(theEmail)

    def export_to_csv(self, thePath, theEvents):
        """
        Export events to a CSV file.
        
        Args:
            thePath: File path where the CSV should be saved.
            theEvents: List of events to export.
            
        Returns:
            bool: True if export was successful, False otherwise.
        """
        from model.db_handler import export_events_to_csv
        return export_events_to_csv(thePath, theEvents)
