import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class FileWatcher:
    def __init__(self, thePath, theEventHandler=LoggingEventHandler(), theRecursive=True):
        self.__myPath = thePath
        self.__myEventHandler = theEventHandler
        self.__myRecursive = theRecursive
        self.__myObserver = None
    
    def start(self):
        self.__myObserver = Observer()
        self.__myObserver.schedule(self.__myEventHandler, self.__myPath, recursive=self.__myRecursive)
        self.__myObserver.start()
        
    def stop(self):
        if self.__myObserver:
            self.__myObserver.stop()
            self.__myObserver.join()
    
    def run(self):
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()