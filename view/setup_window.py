import tkinter as tk
from tkinter import ttk
import os
import datetime
class SetupWindow:
    def __init__(self, theRoot, theController):
        self.myRoot = theRoot
        self.myController = theController

        # Init Window
        theRoot.title('File System Watcher')
        theRoot.geometry('800x800')


        # Directory frame
        directory_frame = tk.Frame(self.myRoot)
        directory_frame.pack(padx=5, pady=5, fill=tk.X)
        # Directory button
        open_directory_button = tk.Button(
            directory_frame,
            text='Open Directory',
            font=('Arial', 16),
            command=self.myController.open_directory
        )
        open_directory_button.pack(side=tk.LEFT, padx=5)
        self.directory_label = tk.Label(
            directory_frame,
            text='No directory selected',
            padx=5,
            pady=5,
            width=60,
            relief=tk.GROOVE,
            borderwidth=2,
            background='white',
        )
        self.directory_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        

        # Control frame
        control_frame = tk.Frame(self.myRoot) 
        control_frame.pack(padx=5, pady=5, anchor=tk.W)
        # Start button
        start_button = tk.Button(
            control_frame,
            text='Start',
            font=('Arial', 16),
            command=theController.start_watching
        )
        start_button.pack(side=tk.LEFT, padx=5)
        # Stop button
        stop_button = tk.Button(
            control_frame,
            text='Stop',
            font=('Arial', 16),
            command=self.myController.stop_watching
        )
        stop_button.pack(side=tk.LEFT)
        # Dropwdown menu to choose which file extension
        self.fileExtensionSelection = tk.StringVar(value='None')
        self.fileExtensionOptions = ['None', '.png', '.txt']
        self.fileExtensionDropdown = tk.OptionMenu(control_frame, 
                                            self.fileExtensionSelection, 
                                            *[opt for opt in self.fileExtensionOptions if opt != self.fileExtensionSelection.get()])
        
        self.fileExtensionDropdown.pack(padx=10, pady=10)
        self.fileExtensionSelection.trace_add('write', self._handle_fileExtension_change)

        # Query Button
        query_button = tk.Button(
            self.myRoot,
            text='Query Database',
            font=('Arial', 20),
            command=self.myController.open_query_window
        )
        query_button.pack(padx=10, pady=20)

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
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=30)


    def add_log(self, theMessage: str):
        arr = theMessage.split(': ')

        event_type = arr[0]
        file_path = arr[1]
        
        filename, extension = os.path.splitext(os.path.basename(file_path))
        if not extension:
            extension = "(none)"
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.tree.insert('', 0, values=(filename, extension, file_path, event_type, timestamp))
        
        # If there are more than 100 items, remove the oldest ones
        if len(self.tree.get_children()) > 100:
            oldest = self.tree.get_children()[-1]
            self.tree.delete(oldest)
    
    def _handle_fileExtension_change(self, *args):
        curr_selection = self.fileExtensionSelection.get()

        self.myController.set_file_extension(curr_selection)
        # Recreate the menu with options that is not selected
        options = [opt for opt in self.fileExtensionOptions if opt != curr_selection]
        menu = self.fileExtensionDropdown['menu']
        menu.delete(0, 'end')
        
        for option in options:
            menu.add_command(
                label=option,
                command=lambda 
                value=option: self.fileExtensionSelection.set(value)
            )
    
    def update_directory_display(self, theDirectory):
        if theDirectory:
            self.directory_label.config(text=f"Selected directory: {theDirectory}")
        else:
            self.directory_label.config(text="No directory selected")