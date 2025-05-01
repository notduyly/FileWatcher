import logging
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info(f'Modified file at: {event.src_path}')
        return super().on_modified(event)
    
    def on_created(self, event):
        logging.info(f'Created file at: {event.src_path}')
        return super().on_created(event)
    
    def on_deleted(self, event):
        logging.info(f'Deleted file at {event.src_path}')
        return super().on_deleted(event)
    
    if __name__ == "__main__":
        print("Testing MyEventHandler...")
        handler = MyEventHandler()
        print("MyEventHandler initialized successfully!")
        print("This module doesn't do anything when run directly.")
        print("It needs to be used with the FileWatcher class.")