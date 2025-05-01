import tkinter as tk
from FileWatcher.model.fileWatcher import FileWatcher
from FileWatcher.model.eventHandler import MyEventHandler

root = tk.Tk()
root.title("File System Watcher")

root.geometry("500x500")

file_watcher = None

def start_watching():
    global file_watcher
    # Create a handler instance
    handler = MyEventHandler()
    # Create and start the file watcher
    file_watcher = FileWatcher('/Users/austinnguyen/Code/FileWatcher', handler)
    file_watcher.start()

def stop_watching():
    global file_watcher
    if file_watcher:
        file_watcher.stop()

# Create buttons with commands
start_button = tk.Button(root, text="Start", font=('Arial', 20), command=start_watching)
start_button.pack(padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", font=('Arial', 20), command=stop_watching)
stop_button.pack(padx=10, pady=10)

root.mainloop()

