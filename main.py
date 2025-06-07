"""
File Watcher Application Entry Point.

The application follows the Model-View-Controller (MVC) architectural pattern:
- Model: Database operations and file system monitoring
- View: Tkinter-based user interface components
- Controller: Business logic and coordination between model and view

Author:
    - Duy Ly ndly@uw.edu
    - Sungmin Cha panda483@uw.edu
    - Austin Nguyen austin11@uw.edu
"""

import tkinter as tk
from controller.main_controller import WatcherController
from view.main_view import FileWatcherGUI

def run():
    """
    Initialize and run the File Watcher application.
    """
    root = tk.Tk()
    controller = WatcherController()
    FileWatcherGUI(root, controller)
    root.mainloop()

if __name__ == "__main__":
    """
    Script entry point.
    """
    run()