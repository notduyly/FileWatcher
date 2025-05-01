import tkinter as tk
import sys
import os


from controller.main_controller import WatcherController
from view.main_view import FileWatcherGUI


def run():
    root = tk.Tk()
    controller = WatcherController()
    FileWatcherGUI(root, controller)
    root.mainloop()

if __name__ == "__main__":
    run()