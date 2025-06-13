import tkinter as tk
from tkinter import ttk
import os
import datetime
from tkinter import messagebox

class SetupWindow:
    """
    Main setup window for the File Watcher application.
    
    Attributes:
        __myRoot: The root Tkinter window instance.
        __myController: The main controller.
        __events_saved: Track if events have been saved
        __directory_label: Label displaying the currently selected directory.
        __fileExtensionSelection: The selected file extension filter.
        __fileExtensionOptions: List of available file extension filter options.
        __fileExtensionDropdown: OptionMenu for selecting file extension filters.
        __tree: TreeView widget for displaying file system events in real-time.
        __start_button: Reference to the start button for state control.
    """
    
    def __init__(self, theRoot, theController):
        """
        Initialize the SetupWindow with root window and controller.
        
        Args:
            theRoot: The root Tkinter window instance.
            theController: The main controller.
        """
        self.__myRoot = theRoot
        self.__myController = theController
        self.__events_saved = True

        # Init Window
        self.__myRoot.title('File System Watcher')
        self.__myRoot.geometry('800x500')

        # Directory frame
        directory_frame = tk.Frame(self.__myRoot)
        directory_frame.pack(padx=5, pady=5, fill=tk.X)
        # Directory button
        open_directory_button = tk.Button(
            directory_frame,
            text='Open Directory',
            font=('Arial', 16),
            command=self.__myController.open_directory,
        )
        open_directory_button.pack(side=tk.LEFT, padx=5)
        self.__directory_label = tk.Label(
            directory_frame,
            text='No directory selected',
            padx=5,
            pady=5,
            width=60,
            relief=tk.GROOVE,
            borderwidth=2,
            bg='white',
            fg='black'
        )
        self.__directory_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        

        # Control frame
        control_frame = tk.Frame(self.__myRoot) 
        control_frame.pack(padx=5, pady=5, anchor=tk.W)
        # Start button
        self.__start_button = tk.Button(
            control_frame,
            text='Start',
            font=('Arial', 16),
            command=theController.start_watching
        )
        self.__start_button.pack(side=tk.LEFT, padx=5)
        # Stop button
        stop_button = tk.Button(
            control_frame,
            text='Stop',
            font=('Arial', 16),
            command=self.__myController.stop_watching
        )
        stop_button.pack(side=tk.LEFT)
        # Dropwdown menu to choose which file extension
        self.__fileExtensionSelection = tk.StringVar(value='None')
        self.__fileExtensionOptions = ['None', '.txt', '.pdf', '.csv', '.docx', '.xlsx', '.png']
        self.__fileExtensionDropdown = tk.OptionMenu(control_frame, 
                                            self.__fileExtensionSelection, 
                                            *[opt for opt in self.__fileExtensionOptions if opt != self.__fileExtensionSelection.get()])
        
        self.__fileExtensionDropdown.pack(side=tk.LEFT, padx=5)
        self.__fileExtensionSelection.trace_add('write', self._handle_fileExtension_change)

        # Query Button
        query_button = tk.Button(
            control_frame,
            text='Query Database',
            font=('Arial', 16),
            command=self.__myController.open_query_window
        )
        query_button.pack(side=tk.LEFT, padx=(250, 5))

        # Save Database Button
        save_button = tk.Button(
            control_frame,
            text='Save Database',
            font=('Arial', 16),
            command=self._save_to_database
        )
        save_button.pack(side=tk.LEFT, padx=5)

        # TextBox to show changes
        cols = ("Filename","Extension","Path","Event","Timestamp")
        self.__tree = ttk.Treeview(self.__myRoot, columns=cols, show='headings')
        for col in cols:
            self.__tree.heading(col, text=col)
            
        self.__tree.column("Filename", width=75, anchor=tk.W)
        self.__tree.column("Extension", width=75, anchor=tk.W)
        self.__tree.column("Path", width=400, anchor=tk.W)
        self.__tree.column("Event", width=100, anchor=tk.W)
        self.__tree.column("Timestamp", width=150, anchor=tk.W)
        
        self.__tree.pack(fill=tk.BOTH, expand=True, pady=30)

        # Bind the window close event
        self.__myRoot.protocol("WM_DELETE_WINDOW", self._on_closing)

    def add_log(self, theMessage: str):
        """
        Adds a file system event log entry to the tree view display.
        
        Args:
            theMessage: Event message.
        """
        arr = theMessage.split(': ')

        event_type = arr[0]
        file_path = arr[1]
        
        filename, extension = os.path.splitext(os.path.basename(file_path))
        if not extension:
            extension = "(none)"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.__tree.insert('', 0, values=(filename, extension, file_path, event_type, timestamp))
        
        # Mark events as unsaved when new events are added
        self.__events_saved = False
        
        # If there are more than 100 items, remove the oldest ones
        if len(self.__tree.get_children()) > 100:
            oldest = self.__tree.get_children()[-1]
            self.__tree.delete(oldest)
    
    def _handle_fileExtension_change(self, *args):
        """
        Handles changes to the file extension filter selection.
        
        Args:
            *args: Variable arguments passed by the StringVar trace callback.
        """
        curr_selection = self.__fileExtensionSelection.get()

        self.__myController.set_file_extension(curr_selection)
        # Recreate the menu with options that is not selected
        options = [opt for opt in self.__fileExtensionOptions if opt != curr_selection]
        menu = self.__fileExtensionDropdown['menu']
        menu.delete(0, 'end')

        for option in options:
            menu.add_command(
                label=option,
                command=lambda value=option: self.__fileExtensionSelection.set(value)
            )
    
    def update_directory_display(self, theDirectory):
        """
        Updates the directory display label with the selected directory path.
        
        Args:
            theDirectory: The directory path to display.
        """
        if theDirectory:
            self.__directory_label.config(text=f"Selected directory: {theDirectory}")
        else:
            self.__directory_label.config(text="No directory selected")
    
    def _save_to_database(self):
        """
        Saves currently displayed events to the database.
        """
        if not self.__tree.get_children():
            messagebox.showwarning("Warning", "No events to save.")
            return
            
        if messagebox.askyesno("Confirm Save", 
                            "Do you want to save these events to the database?\n"
                            "This will add new events to existing data."):
            events = []
            for item in self.__tree.get_children():
                values = self.__tree.item(item)['values']
                events.append({
                    'filepath': values[2],
                    'event_type': values[3],
                })
            
            if self.__myController.save_events_to_database(events):
                messagebox.showinfo("Success", "Events saved to database.")
                # Mark events as saved
                self.__events_saved = True
                # Clear the logs after save
                for item in self.__tree.get_children():
                    self.__tree.delete(item)
            else:
                messagebox.showerror("Error", "Failed to save events to database")
    
    def _on_closing(self):
        """
        Handle the window closing event.
        
        Prompts user to save unsaved events before closing the application.
        """
        if self.__tree.get_children() and not self.__events_saved:
            result = messagebox.askyesnocancel(
                "Unsaved Events", 
                "You have unsaved events. Do you want to save them before closing?"
            )
            
            if result is True:
                self._save_to_database()
                if self.__events_saved:
                    self.__myRoot.destroy()
            elif result is False:
                self.__myRoot.destroy()
        else:
            self.__myRoot.destroy()

    def set_start_button_state(self, enabled):
        """
        Enable or disable the start button.
        
        Args:
            enabled: True to enable the button, False to disable it.
        """
        if enabled:
            self.__start_button.config(state='normal')
        else:
            self.__start_button.config(state='disabled')