import sys
import os

from model.fileWatcher import FileWatcher
from model.eventHandler import MyEventHandler
from tkinter import filedialog, messagebox

class WatcherController:
    def __init__(self):
        self.watcher = None
        self.view = None
        self.watch_directory = ''

    def set_view(self, view):
        self.view = view

    def start_watching(self):
        if self.watcher:
            print("Already watching.")
            return
        for file in self.watch_directory:
            handler = MyEventHandler(logToTextbox=self.view.add_log)
            self.watcher = FileWatcher(file, handler)
            self.watcher.start()
            print(f"Started watching directory: {self.watch_directory}")
    
    def stop_watching(self):
        if self.watcher:
            self.watcher.stop()
            self.watcher = None
            print("Stopped watching")

    def open_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            # 이전 감시 중지
            if self.watcher:
                self.stop_watching()
                
            self.watch_directory = [directory]
            if self.view:
                self.view.update_directory_view(directory)
                
            # 하위 디렉토리 포함하여 감시 시작
            handler = MyEventHandler(logToTextbox=self.view.add_log)
            self.watcher = FileWatcher(directory, handler)
            self.watcher.start()
            
            # 하위 디렉토리 정보 출력
            subdirs = [x[0] for x in os.walk(directory)][1:]
            if subdirs:
                print(f"Including subdirectories:")
                for subdir in subdirs:
                    print(f" - {os.path.basename(subdir)}")
