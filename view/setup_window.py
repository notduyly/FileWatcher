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
        self.root.after(100, self.process_log_queue)

        # Init Window
        root.title('File System Watcher')
        root.geometry('800x800')

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

        # Dropdown menu to choose which file extension
        self.fileExtensionSelection = tk.StringVar(value='None')
        self.fileExtensionOptions = ['None', '.png', '.txt']
        self.fileExtensionDropdown = tk.OptionMenu(root,
                                                   self.fileExtensionSelection,
                                                   *[opt for opt in self.fileExtensionOptions if opt != self.fileExtensionSelection.get()])
        self.fileExtensionDropdown.pack(padx=10, pady=10)
        self.fileExtensionSelection.trace_add('write', self.handle_fileExtension_change)

        # TextBox to show changes
        cols = ("Filename", "Extension", "Path", "Event", "Timestamp")
        self.tree = ttk.Treeview(root, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Separate section for file system events
        ttk.Label(root, text="File System Events", font=('Arial', 12, 'bold')).pack(pady=5)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def add_log(self, message: str):
        arr = message.split(': ', 1)
        if len(arr) < 2:
            return  # 예외 처리

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
                    
            # 감시 중인 디렉토리 레이블 업데이트
            subdir_count = len([x[0] for x in os.walk(directory)][1:])
            if subdir_count > 0:
                self.watch_label.config(
                    text=f"Watching: {directory}\nIncluding {subdir_count} subdirectories"
                )
            else:
                self.watch_label.config(text=f"Watching: {directory}")
                
        except Exception as e:
            print(f"Error updating directory view: {e}")