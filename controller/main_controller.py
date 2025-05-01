import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler

class WatcherController:
    def __init__(self):
        self.watcher = None
        self.watch_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "testFileToWatch")

    def start_watching(self):
        handler = MyEventHandler()
        self.watcher = FileWatcher(self.watch_directory, handler)
        self.watcher.start()
        print(f"Started watching directory: {self.watch_directory}")
    
    def stop_watching(self):
        if self.watcher:
            self.watcher.stop()
            print("Stopped watching")