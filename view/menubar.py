import tkinter as tk
from tkinter import Menu, messagebox
from model import fileWatcher

class MenuBar:
    """
    Menu bar component for the File Watcher application.
    
    Attributes:
        __myRoot: The root Tkinter window instance.
        __myController: The main controller instance for handling menu actions.
        __myMenubar: The Tkinter Menu instance representing the menu bar.
    """
    
    def __init__(self, theRoot, theController):
        """
        Initialize the MenuBar with root window and controller.
        
        Args:
            theRoot: The root Tkinter window instance.
            theController: The main controller.
        """
        self.__myRoot = theRoot
        self.__myController = theController
        self.__myMenubar = Menu(self.__myRoot)
        self._create()

    def _create(self):
        """
        Creates complete menu bar structure with all menus and keyboard shortcuts.
        
        Creates the following menus:
        - File: Open directory, Exit application
        - File System Watcher: Start/Stop watching operations
        - Database: Query and save database operations
        - About: Developer info, version, and usage instructions
        
        Also binds keyboard shortcuts:
        - Ctrl+O: Open directory
        - Ctrl+R: Start watching
        - Ctrl+S: Stop watching
        - Ctrl+F: Query database
        - Ctrl+D: Save to database
        - Ctrl+Q: Exit application
        """
        # File menu
        file_menu = Menu(self.__myMenubar, tearoff=0)
        file_menu.add_command(label="Open", 
                            command=self.__myController.open_directory,
                            accelerator="Ctrl+o")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", 
                            command=self.exit_app,
                            accelerator="Ctrl+q")
        self.__myMenubar.add_cascade(label="File", menu=file_menu)

        # File System Watcher menu
        fsw_menu = Menu(self.__myMenubar, tearoff=0)
        fsw_menu.add_command(label="Start watching", 
                            command=self.__myController.start_watching,
                            accelerator="Ctrl+r")
        fsw_menu.add_command(label="Stop watching",
                            command=self.__myController.stop_watching,
                            accelerator="Ctrl+s")
        self.__myMenubar.add_cascade(label="File System Watcher", menu=fsw_menu)

        # Database menu
        db_menu = Menu(self.__myMenubar, tearoff=0)
        db_menu.add_command(label="Query database",
                            command=self.__myController.open_query_window,
                            accelerator="Ctrl+f")
        db_menu.add_command(label="Save to database",
                            command=lambda event: self.__myController.get_view().save_to_database(),
                            accelerator="Ctrl+d"
                            )
        self.__myMenubar.add_cascade(label="Database", menu=db_menu)

        # About menu
        ab_menu = Menu(self.__myMenubar, tearoff=0)
        ab_menu.add_command(label="Developers", command=self.show_developers)
        ab_menu.add_command(label="Version", command=self.show_version)
        ab_menu.add_command(label="How to use", command=self.show_how_to_use)
        self.__myMenubar.add_cascade(label="About", menu=ab_menu)

        self.__myRoot.bind_all('<Control-r>', lambda event: self.__myController.start_watching())
        self.__myRoot.bind_all('<Control-s>', lambda event: self.__myController.stop_watching())
        self.__myRoot.bind_all('<Control-o>', lambda event: self.__myController.open_directory())
        self.__myRoot.bind_all('<Control-f>', lambda event: self.__myController.open_query_window())
        self.__myRoot.bind_all('<Control-d>', lambda event: self.__myController.get_view().save_to_database())
        self.__myRoot.bind_all('<Control-q>', lambda event:self.exit_app())

    def show_developers(self):
        """
        Displays information about the application developers.
        """
        messagebox.showinfo("Developers", "Developed by:\nDuy Ly\nSungmin Cha\nAustin Nguyen")

    def show_version(self):
        """
        Displays information about the application version.
        """
        messagebox.showinfo("Version", "FileWatcher v1.0.0\nBuild date: Spring 2025")

    def show_how_to_use(self):
        """
        Displays usage instructions for the application.
        """
        messagebox.showinfo(
            "How to Use",
            "1. Select a directory to watch.\n"
            "2. File changes of that directory will be logged.\n"
            "3. Use the Database menu to query or save events.\n"
            "4. Save a CSV file to your email."
        )

    def get_menubar(self):
        """
        Gets the menu bar instance for attachment to the main window.
        
        Returns:
            Menu: The Tkinter Menu instance representing the complete menu bar.
        """
        return self.__myMenubar

    def exit_app(self):
        """
        Exit the application.
        """
        import sys
        sys.exit()

