import tkinter as tk
from tkinter import Menu, messagebox

from model import fileWatcher

class MenuBar:
    
    def __init__(self, theRoot, theController):
        self.__myRoot = theRoot
        self.__controller = theController
        self.__myMenubar = Menu(self.__myRoot)
        self._create()

# System menu bar
    def _create(self):
        # File menu
        file_menu = Menu(self.__myMenubar, tearoff=0)
        file_menu.add_command(label="Open", 
                              command=self.__controller.open_directory,
                              accelerator="Ctrl+o")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", 
                              command=self.exit_app,
                              accelerator="Ctrl+q")
        self.__myMenubar.add_cascade(label="File", menu=file_menu)

        # File System Watcher menu
        fsw_menu = Menu(self.__myMenubar, tearoff=0)
        fsw_menu.add_command(label="Start watching", 
                             command=self.__controller.start_watching,
                             accelerator="Ctrl+r")
        fsw_menu.add_command(label="Stop watching",
                             command=self.__controller.stop_watching,
                             accelerator="Ctrl+s")
        self.__myMenubar.add_cascade(label="File System Watcher", menu=fsw_menu)

        # Database menu
        db_menu = Menu(self.__myMenubar, tearoff=0)
        db_menu.add_command(label="Query database",
                            command=self.__controller.open_query_window,
                            accelerator="Ctrl+f")
        db_menu.add_command(label="Save to database")
        self.__myMenubar.add_cascade(label="Database", menu=db_menu)

        # About menu
        ab_menu = Menu(self.__myMenubar, tearoff=0)
        ab_menu.add_command(label="Developers", command=self.show_developers)
        ab_menu.add_command(label="Version", command=self.show_version)
        ab_menu.add_command(label="How to use", command=self.show_how_to_use)
        self.__myMenubar.add_cascade(label="About", menu=ab_menu)

        self.__myRoot.bind_all('<Control-r>', lambda event: self.__controller.start_watching())
        self.__myRoot.bind_all('<Control-s>', lambda event: self.__controller.stop_watching())
        self.__myRoot.bind_all('<Control-o>', lambda event: self.__controller.open_directory())
        self.__myRoot.bind_all('<Control-f>', lambda event: self.__controller.open_query_window())
        self.__myRoot.bind_all('<Control-q>', lambda event:self.exit_app())


    def show_developers(self):
            messagebox.showinfo("Developers", "Developed by:\nDuy Ly\nSungmin Cha\nAustin Nguyen")

    def show_version(self):
        messagebox.showinfo("Version", "FileWatcher v1.0.0\nBuild date: Spring 2025")

    def show_how_to_use(self):
        messagebox.showinfo(
            "How to Use",
            "1. Select a directory to watch.\n"
            "2. File changes of that directory will be logged.\n"
            "3. Use the Database menu to query or save events.\n"
            "4. Save a CSV file to your email."
        )

    def get_menubar(self):
        return self.__myMenubar

    def exit_app(self):
        import sys
        sys.exit()


    


