import tkinter as tk
from tkinter import Menu
from .query_window import QueryWindow

class MenuBar:
    
    def __init__(self, root):
        self.root = root
        self.menubar = Menu(self.root)
        self.create()


# System menu bar
    def create(self):
        # File menu
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.menubar.add_cascade(label="File", menu=file_menu)

        # File System Watcher menu
        fsw_menu = Menu(self.menubar, tearoff=0)
        fsw_menu.add_command(label="Start watching")
        fsw_menu.add_command(label="Stop watching")
        self.menubar.add_cascade(label="File System Watcher", menu=fsw_menu)

        # Database menu
        db_menu = Menu(self.menubar, tearoff=0)
        db_menu.add_command(label="Save to database")
        self.menubar.add_cascade(label="Database", menu=db_menu)

        # About menu
        ab_menu = Menu(self.menubar, tearoff=0)
        ab_menu.add_command(label="Developers")
        ab_menu.add_command(label="Version")
        ab_menu.add_command(label="How to use")
        self.menubar.add_cascade(label="About", menu=ab_menu)

    def get_menubar(self):
        return self.menubar

    def exit_app(self):
        import sys
        sys.exit()