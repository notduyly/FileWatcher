import logging
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Inherits from FileSystemEventHandler. We override these
# methods to handle how we react to file changes.
class MyEventHandler(FileSystemEventHandler):
    def __init__(self, logToTextbox=None):
        super().__init__()
        self.logToTextbox = logToTextbox
    
    def on_modified(self, event):
        msg = f'Modified file at: {event.src_path}'
        if self.logToTextbox:
            self.logToTextbox(msg)
        return super().on_modified(event)
    
    def on_created(self, event):
        msg = f'Created file at: {event.src_path}'
        if self.logToTextbox:
            self.logToTextbox(msg)
        return super().on_created(event)
    
    def on_deleted(self, event):
        msg = f'Deleted file at {event.src_path}'
        if self.logToTextbox:
            self.logToTextbox(msg)
        return super().on_deleted(event)
