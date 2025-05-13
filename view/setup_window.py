import tkinter as tk

class setupWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Init Window
        root.title('File System Watcher')
        root.geometry('500x500')

        # Start/Stop button
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

        # Dropwdown menu to choose which file extension
        self.fileExtensionSelection = tk.StringVar(value='')
        fileExtensionOptions = ['', '.txt']
        fileExtensionDropdown = tk.OptionMenu(root, self.fileExtensionSelection, *fileExtensionOptions)
        fileExtensionDropdown.pack(padx=10, pady=10)

        self.fileExtensionSelection.trace_add('write', self.on_extension_change)

        # Log to TextBox
        self.log_text = tk.Text(self.root, state='disabled', wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)

    def add_log(self, message: str):
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')
    
    def on_extension_change(self, *args):
        extension = self.fileExtensionSelection.get()
    