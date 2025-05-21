import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class FileWatcher:
    def __init__(self, thePath, theEventHandler=LoggingEventHandler(), theRecursive=True):
        self.myPath = thePath
        self.myEventHandler = theEventHandler
        self.myRecursive = theRecursive
        self.myObserver = None
    
    def start(self):
        self.myObserver = Observer()
        self.myObserver.schedule(self.myEventHandler, self.myPath, recursive=self.myRecursive)
        self.myObserver.start()
        
    def stop(self):
        if self.myObserver:
            self.myObserver.stop()
            self.myObserver.join()
    
    def run(self):
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()