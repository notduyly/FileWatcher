import tkinter as tk
from tkinter import Menu

class MenuBar:
    
    def __init__(self, root):
        self.root = root
        self.create()

    def create(self):
        self.menubar_frame = tk.Frame(self.root, height=30)
        self.menubar_frame.pack(fill=tk.X)

        file_button = tk.Button(self.menubar_frame, text="File", command=self.file_menu, bg="lightgray")
        file_button.pack(side=tk.LEFT, padx=5, pady=2)

        fsw_button = tk.Button(self.menubar_frame, text="File System Watcher", command=self.fsw_menu, bg="lightgray")
        fsw_button.pack(side=tk.LEFT, padx=5, pady=2)

        db_button = tk.Button(self.menubar_frame, text="Database", command=self.db_menu, bg="lightgray")
        db_button.pack(side=tk.LEFT, padx=5, pady=2)

        about_button = tk.Button(self.menubar_frame, text="About", command=self.about_menu, bg="lightgray")
        about_button.pack(side=tk.LEFT, padx=5, pady=2)

    def file_menu(self):
        file_menu = tk.Menu(self.root, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.show_popup(file_menu)

    def fsw_menu(self):
        fsw_menu = tk.Menu(self.root, tearoff=0)
        fsw_menu.add_command(label="Start watching")
        fsw_menu.add_command(label="Stop watching")
        self.show_popup(fsw_menu)

    def db_menu(self):
        db_menu = tk.Menu(self.root, tearoff=0)
        db_menu.add_command(label="Save to database")
        self.show_popup(db_menu)

    def about_menu(self):
        about_menu = tk.Menu(self.root, tearoff=0)
        about_menu.add_command(label="Developers")
        about_menu.add_command(label="Version")
        about_menu.add_command(label="How to use")
        self.show_popup(about_menu)

    def show_popup(self, menu):
        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        menu.post(x, y)
    
    def exit_app(self):
        self.root.destroy()


# System menu bar
    # def create(self):
    #     # File menu
    #     file_menu = Menu(self.menubar, tearoff=0)
    #     file_menu.add_command(label="Open")
    #     file_menu.add_command(label="Save")
    #     file_menu.add_separator()
    #     file_menu.add_command(label="Exit", command=self.exit_app)
    #     self.menubar.add_cascade(label="File", menu=file_menu)

    #     # File System Watcher menu
    #     fsw_menu = Menu(self.menubar, tearoff=0)
    #     fsw_menu.add_command(label="Start watching")
    #     fsw_menu.add_command(label="Stop watching")
    #     self.menubar.add_cascade(label="File System Watcher", menu=fsw_menu)

    #     # Database menu
    #     db_menu = Menu(self.menubar, tearoff=0)
    #     db_menu.add_command(label="Save to database")
    #     self.menubar.add_cascade(label="Database", menu=db_menu)

    #     # About menu
    #     ab_menu = Menu(self.menubar, tearoff=0)
    #     ab_menu.add_command(label="Developers")
    #     ab_menu.add_command(label="Version")
    #     ab_menu.add_command(label="How to use")
    #     self.menubar.add_cascade(label="About", menu=ab_menu)

    # def get_menubar(self):
    #     return self.menubar

    # def exit_app(self):
    #     import sys
    #     sys.exit()

