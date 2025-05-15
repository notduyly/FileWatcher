import tkinter as tk
from tkinter import ttk
import os
import datetime
class setupWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Init Window
        root.title('File System Watcher')
        root.geometry('500x500')

        # Start/Stop and Directory buttons
        start_button = tk.Button(
            self.root,
            text='Start',
            font=('Arial', 20),
            command=controller.start_watching
        )
        start_button.pack(padx=10, pady=10)
        stop_button = tk.Button(
            self.root,
            text='Stop',
            font=('Arial', 20),
            command=self.controller.stop_watching
        )
        stop_button.pack(padx=10, pady=20)

        open_directory_button = tk.Button(
            self.root,
            text='Open Directory',
            font=('Arial', 20),
            command=self.controller.open_directory
        )
        open_directory_button.pack(padx=10, pady=20)


        # Dropwdown menu to choose which file extension
        self.fileExtensionSelection = tk.StringVar(value='None')
        self.fileExtensionOptions = ['None', '.png', '.txt']
        self.fileExtensionDropdown = tk.OptionMenu(root, 
                                            self.fileExtensionSelection, 
                                            *[opt for opt in self.fileExtensionOptions if opt != self.fileExtensionSelection.get()])
        
        self.fileExtensionDropdown.pack(padx=10, pady=10)
        self.fileExtensionSelection.trace_add('write', self.handle_fileExtension_change)

        cols = ("Filename","Extension","Path","Event","Timestamp")
        self.tree = ttk.Treeview(root, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Log to TextBox
        self.log_text = tk.Text(self.root, state='disabled', wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)


    def add_log(self, message: str):
        # self.log_text.config(state='normal')
        # self.log_text.insert('end', message + '\n')
        # self.log_text.see('end')
        # self.log_text.config(state='disabled')
        print(message)
        arr = message.split()
        
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
    
    def handle_fileExtension_change(self, *args):
        curr_selection = self.fileExtensionSelection.get()

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
    