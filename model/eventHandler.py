import logging
from watchdog.events import FileSystemEventHandler
from .db_handler import insert_event

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class MyEventHandler(FileSystemEventHandler):
    """
    Custom file system event handler that monitors and logs file changes.
    
    This class extends the watchdog FileSystemEventHandler to provide
    custom handling of file system events.
    """
    
    def __init__(self, logToTextbox=None):
        """
        Initialize the event handler.
        
        Args:
            logToTextbox: Function to call for logging events to the View.
        """
        super().__init__()
        self.__myLogToTextbox = logToTextbox
        self.__myExtensionFilter = ''

    def set_extension_filter(self, theExtension):
        """
        Sets the file extension filter.
        
        Args:
            theExtension: File extension to filter by ('.txt', '.png').
        """
        self.__myExtensionFilter = theExtension

    def on_modified(self, theEvent):
        """
        Handles file modification events.
        
        Args:
            theEvent: The file system event object.
            
        Returns:
            The result of calling the parent class' on_modified method.
        """
        msg = f'Modified: {theEvent.src_path}'
        if self.__myLogToTextbox:
            self.__myLogToTextbox(msg)
        return super().on_modified(theEvent)

    def on_created(self, theEvent):
        """
        Handles file creation events.
        
        Args:
            theEvent: The file system event object.
            
        Returns:
            The result of calling the parent class' on_created method.
        """
        msg = f'Created: {theEvent.src_path}'
        if self.__myLogToTextbox:
            self.__myLogToTextbox(msg)
        return super().on_created(theEvent)

    def on_deleted(self, theEvent):
        """
        Handles file deletion events.
        
        Args:
            theEvent: The file system event object.
            
        Returns:
            The result of calling the parent class' on_deleted method.
        """
        msg = f'Deleted: {theEvent.src_path}'
        if self.__myLogToTextbox:
            self.__myLogToTextbox(msg)
        return super().on_deleted(theEvent)

    def dispatch(self, theEvent):
        """
        Dispatch file system events with optional extension filtering.
        
        Args:
            theEvent: The file system event to dispatch.
            
        Returns:
            The result of calling the parent class' dispatch method or None.
        """
        if self.__myExtensionFilter and self.__myExtensionFilter != 'None':
            if theEvent.src_path.lower().endswith(self.__myExtensionFilter.lower()):
                return super().dispatch(theEvent)
        else: 
            return super().dispatch(theEvent)
