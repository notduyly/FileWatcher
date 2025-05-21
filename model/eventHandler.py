import logging
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, logToTextbox=None):
        super().__init__()
        self.logToTextbox = logToTextbox
    
    def _log_event(self, event_type, path):
        """Common logging function"""
        msg = f'{event_type}: {path}'
        if self.logToTextbox:
            self.logToTextbox(msg)
    
    def on_modified(self, event):
        self._log_event('Modified', event.src_path)
        return super().on_modified(event)
    
    def on_created(self, event):
        self._log_event('Created', event.src_path)
        return super().on_created(event)
    
    def on_deleted(self, event):
        self._log_event('Deleted', event.src_path)
        return super().on_deleted(event)
