import queue
import tkinter as tk
from tkinter import ttk
import os
import datetime

class setupWindow:
    def __init__(self, theRoot, theController):
        self.myRoot = theRoot
        self.myController = theController

        # Init Window
        theRoot.title('File System Watcher')
        theRoot.geometry('800x800')

        # Start/Stop and Directory buttons
        start_button = tk.Button(
            self.myRoot,
            text='Start',
            font=('Arial', 20),
            command=theController.start_watching
        )
        start_button.pack(padx=10, pady=10)

        stop_button = tk.Button(
            self.myRoot,
            text='Stop',
            font=('Arial', 20),
            command=self.myController.stop_watching
        )
        stop_button.pack(padx=10, pady=20)

        # Directory
        open_directory_button = tk.Button(
            self.myRoot,
            text='Open Directory',
            font=('Arial', 20),
            command=self.myController.open_directory
        )
        open_directory_button.pack(padx=10, pady=20)
        self.directory_label = tk.Label(
            self.myRoot,
            text='No directory selected',
            padx=5,
            pady=5,
            width=70,
            relief=tk.GROOVE,
            borderwidth=2,
            background='white',
        )
        self.directory_label.pack(padx=10, pady=10)

        # Dropwdown menu to choose which file extension
        self.fileExtensionSelection = tk.StringVar(value='None')
        self.fileExtensionOptions = ['None', '.png', '.txt']
        self.fileExtensionDropdown = tk.OptionMenu(self.myRoot, 
                                            self.fileExtensionSelection, 
                                            *[opt for opt in self.fileExtensionOptions if opt != self.fileExtensionSelection.get()])
        
        self.fileExtensionDropdown.pack(padx=10, pady=10)
        self.fileExtensionSelection.trace_add('write', self.handle_fileExtension_change)

        # TextBox to show changes
        cols = ("Filename","Extension","Path","Event","Timestamp")
        self.tree = ttk.Treeview(self.myRoot, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            
        self.tree.column("Filename", width=75, anchor=tk.W)
        self.tree.column("Extension", width=75, anchor=tk.W)
        self.tree.column("Path", width=400, anchor=tk.W)
        self.tree.column("Event", width=100, anchor=tk.W)
        self.tree.column("Timestamp", width=150, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Separate section for file system events
        ttk.Label(self.root, text="File System Events", font=('Arial', 12, 'bold')).pack(pady=5)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def add_log(self, theMessage: str):
        arr = theMessage.split(': ')

        event_type = arr[0]
        file_path = arr[1]
        
        filename, extension = os.path.splitext(os.path.basename(file_path))
        if not extension:
            extension = "(none)"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log_data = {
            "filename": filename,
            "extension": extension,
            "file_path": file_path,
            "event_type": event_type,
            "timestamp": timestamp
        }

        self.log_queue.put(log_data)

    def process_log_queue(self):
        while not self.log_queue.empty():
            log_data = self.log_queue.get()

            self.tree.insert('', 0, values=(
                log_data["filename"],
                log_data["extension"],
                log_data["file_path"],
                log_data["event_type"],
                log_data["timestamp"]
            ))

            # Keep only last 100 items
            if len(self.tree.get_children()) > 100:
                oldest = self.tree.get_children()[-1]
                self.tree.delete(oldest)

        self.root.after(100, self.process_log_queue)

    def handle_fileExtension_change(self, *args):
        curr_selection = self.fileExtensionSelection.get()

        self.myController.set_file_extension(curr_selection)
        # Recreate the menu with options that is not selected
        options = [opt for opt in self.fileExtensionOptions if opt != curr_selection]
        menu = self.fileExtensionDropdown['menu']
        menu.delete(0, 'end')

        for option in options:
            menu.add_command(
                label=option,
                command=lambda value=option: self.fileExtensionSelection.set(value)
            )
    
    def update_directory_display(self, theDirectory):
        if theDirectory:
            self.directory_label.config(text=f"Selected directory: {theDirectory}")
        else:
            self.directory_label.config(text="No directory selected")
