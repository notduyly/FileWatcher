import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class FileWatcher:
    def __init__(self, directory, handler):
        self.directory = directory
        self.handler = handler
        self.observer = None

    def start(self):
        try:
            self.observer = Observer()
            # recursive=True로 설정하여 하위 디렉토리도 감시
            self.observer.schedule(self.handler, self.directory, recursive=True)
            self.observer.start()
            print(f"Started watching {self.directory} and its subdirectories")
        except Exception as e:
            print(f"Error starting observer: {e}")
        
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