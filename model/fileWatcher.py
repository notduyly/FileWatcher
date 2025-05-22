import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import logging

class FileWatcher:
    def __init__(self, directory, handler):
        self.directory = directory
        self.handler = handler
        self.observer = None
        self.logger = logging.getLogger(__name__)

    def start(self):
        try:
            if self.observer is not None:
                self.logger.warning("Observer already exists. Stopping previous observer.")
                self.stop()
                
            self.observer = Observer()
            # recursive=True로 설정하여 하위 디렉토리도 감시
            self.observer.schedule(self.handler, self.directory, recursive=True)
            self.observer.start()
            self.logger.info(f"Started watching {self.directory} and its subdirectories")
        except Exception as e:
            self.logger.error(f"Error starting observer: {e}")
            self.stop()
            raise
        
    def stop(self):
        if self.observer:
            try:
                self.observer.stop()
                self.observer.join()
                self.observer = None
                self.logger.info("Stopped watching directory")
            except Exception as e:
                self.logger.error(f"Error stopping observer: {e}")
    
    def run(self):
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self.logger.error(f"Error in run loop: {e}")
            self.stop()