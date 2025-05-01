import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class FileWatcher:
    def __init__(self, path, event_handler=LoggingEventHandler(), recursive=True):
        self.path = path
        self.event_handler = event_handler
        self.recursive = recursive
        self.observer = None
    
    def start(self):
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=self.recursive)
        self.observer.start()
        
    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
    
    def run(self):
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()