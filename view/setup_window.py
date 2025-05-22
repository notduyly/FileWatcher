import queue
import tkinter as tk
from tkinter import ttk
import os
import datetime

class setupWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.log_queue = queue.Queue()
        
        # Init Window
        self._init_window()
        # Setup UI Components
        self._setup_buttons()
        self._setup_file_extension_dropdown()
        self._setup_treeview()
        
        # Start queue processing
        self.root.after(100, self.process_log_queue)
        
    def _init_window(self):
        """Initialize window properties"""
        self.root.title('File System Watcher')
        self.root.geometry('800x800')
        
    def _setup_buttons(self):
        """Setup control buttons"""
        buttons = [
            ('Start', self.controller.start_watching),
            ('Stop', self.controller.stop_watching),
            ('Open Directory', self.controller.open_directory)
        ]
        
        for text, command in buttons:
            tk.Button(
                self.root,
                text=text,
                font=('Arial', 20),
                command=command
            ).pack(padx=10, pady=10)
            
    def _setup_file_extension_dropdown(self):
        """Setup file extension dropdown"""
        self.fileExtensionSelection = tk.StringVar(value='None')
        self.fileExtensionOptions = ['None', '.png', '.txt']
        self.fileExtensionDropdown = tk.OptionMenu(
            self.root,
            self.fileExtensionSelection,
            *self.fileExtensionOptions
        )
        self.fileExtensionDropdown.pack(padx=10, pady=10)
        self.fileExtensionSelection.trace_add('write', self.handle_fileExtension_change)
        
    def _setup_treeview(self):
        """Setup treeview for event logging"""
        cols = ("Filename", "Extension", "Path", "Event", "Timestamp")
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings')
        
        # Configure columns
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.W)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack components
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_log(self, message: str):
        arr = message.split(': ', 1)
        if len(arr) < 2:
            return

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
        options = [opt for opt in self.fileExtensionOptions if opt != curr_selection]
        menu = self.fileExtensionDropdown['menu']
        menu.delete(0, 'end')

        for option in options:
            menu.add_command(
                label=option,
                command=lambda value=option: self.fileExtensionSelection.set(value)
            )

    def update_directory_view(self, directory):
        # Clear existing items
        for item in self.directory_tree.get_children():
            self.directory_tree.delete(item)
            
        try:
            # 메인 디렉토리와 하위 디렉토리 표시
            for root, dirs, files in os.walk(directory):
                # 디렉토리 항목 추가
                for d in dirs:
                    full_path = os.path.join(root, d)
                    modified = datetime.datetime.fromtimestamp(
                        os.path.getmtime(full_path)
                    ).strftime('%Y-%m-%d %H:%M:%S')
                    
                    self.directory_tree.insert('', 'end', values=(
                        d,
                        "<DIR>",
                        "-",
                        modified
                    ))
                
                # 파일 항목 추가
                for f in files:
                    full_path = os.path.join(root, f)
                    extension = os.path.splitext(f)[1] or "(none)"
                    size = f"{os.path.getsize(full_path):,} bytes"
                    modified = datetime.datetime.fromtimestamp(
                        os.path.getmtime(full_path)
                    ).strftime('%Y-%m-%d %H:%M:%S')
                    
                    self.directory_tree.insert('', 'end', values=(
                        f,
                        extension,
                        size,
                        modified
                    ))
                
        except Exception as e:
            print(f"Error updating directory view: {e}")