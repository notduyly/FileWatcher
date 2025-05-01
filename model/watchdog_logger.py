import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import init_db, insert_event

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            file_size = os.path.getsize(event.src_path)
            insert_event(filename, "created", file_size)
            print(f"[CREATED] {filename} ({file_size} bytes)")
            
    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            try:
                file_size = os.path.getsize(event.src_path)
            except FileNotFoundError:
                file_size = 0
            insert_event(filename, "modified", file_size)
            print(f"[MODIFIED] {filename} ({file_size} bytes)")
            
    def on_deleted(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            insert_event(filename, "deleted", 0)
            print(f"[DELETED] {filename}")
            
def start_watch(path_to_watch="."):
    print(f"📁 Monitoring directory: {path_to_watch}")
    init_db()
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n Monitoring stopped.")
    observer.join()
    
if __name__ == "__main__":
    watch_path = "./watch_folder"
    os.makedirs(watch_path, exist_ok=True)
    start_watch(watch_path)
