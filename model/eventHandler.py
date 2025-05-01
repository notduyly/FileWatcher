import logging
from watchdog.events import FileSystemEventHandler
from db_handler import insert_event

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info(f'Modified file at: {event.src_path}')
        insert_event("Modified", event.src_path, is_directory=event.is_directory)
        return super().on_modified(event)
    
    def on_created(self, event):
        logging.info(f'Created file at: {event.src_path}')
        insert_event("Created", event.src_path, is_directory=event.is_directory)
        return super().on_created(event)
    
    def on_deleted(self, event):
        logging.info(f'Deleted file at {event.src_path}')
        insert_event("Deleted", event.src_path, is_directory=event.is_directory)
        return super().on_deleted(event)
