import tkinter as tk
from tkinter import Menu

from model import fileWatcher

class MenuBar:
    
    def __init__(self, theRoot):
        self.__myRoot = theRoot
        self.__myMenubar = Menu(self.__myRoot)
        self._create()

# System menu bar
    def _create(self):
        # File menu
        file_menu = Menu(self.__myMenubar, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.__myMenubar.add_cascade(label="File", menu=file_menu)

        # File System Watcher menu
        fsw_menu = Menu(self.__myMenubar, tearoff=0)
        fsw_menu.add_command(label="Start watching")
        fsw_menu.add_command(label="Stop watching")
        self.__myMenubar.add_cascade(label="File System Watcher", menu=fsw_menu)

        # Database menu
        db_menu = Menu(self.__myMenubar, tearoff=0)
        db_menu.add_command(label="Save to database")
        self.__myMenubar.add_cascade(label="Database", menu=db_menu)

        # About menu
        ab_menu = Menu(self.__myMenubar, tearoff=0)
        ab_menu.add_command(label="Developers")
        ab_menu.add_command(label="Version")
        ab_menu.add_command(label="How to use")
        self.__myMenubar.add_cascade(label="About", menu=ab_menu)

    def get_menubar(self):
        return self.__myMenubar

    def exit_app(self):
        import sys
        sys.exit()

