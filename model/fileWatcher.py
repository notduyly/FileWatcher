import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class FileWatcher:
    """
    A file system watcher that monitors directory changes using the watchdog library.
    
    Attributes:
        __myPath: The directory path to monitor.
        __myEventHandler: The event handler to process file system events.
        __myRecursive: Whether to monitor subdirectories recursively.
        __myObserver: The watchdog Observer instance for monitoring.
    """
    
    def __init__(self, thePath, theEventHandler=LoggingEventHandler(), theRecursive=True):
        """
        Initialize the FileWatcher with specified path and event handler.
        
        Args:
            thePath: The directory path to monitor.
            theEventHandler: Custom event handler. Defaults to LoggingEventHandler().
            theRecursive: Whether to monitor subdirectories recursively. Defaults to True.
        """
        self.__myPath = thePath
        self.__myEventHandler = theEventHandler
        self.__myRecursive = theRecursive
        self.__myObserver = None
    
    def start(self):
        """
        Start monitoring the specified directory.
        
        Note:
            This method is non-blocking. The observer runs in a separate thread.
        """
        self.__myObserver = Observer()
        self.__myObserver.schedule(self.__myEventHandler, self.__myPath, recursive=self.__myRecursive)
        self.__myObserver.start()
        
    def stop(self):
        """
        Stop monitoring the directory and clean up resources.
        
        Note:
            It's safe to call this method even if the observer is not running.
        """
        if self.__myObserver:
            self.__myObserver.stop()
            self.__myObserver.join()
    
    def run(self):
        """
        Start monitoring and keep the watcher running indefinitely.
        
        Note:
            This is a blocking method that will run until manually interrupted.
            Use start() and stop() methods for more granular control.
            
        Raises:
            KeyboardInterrupt: Caught and handled to gracefully stop the watcher.
        """
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()