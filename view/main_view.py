import tkinter as tk
import sys
import os
from .setup_window import setupWindow

class FileWatcherGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.controller.set_view(self)
        self.window = setupWindow(root, controller)

    def add_log(self, message):
        self.window.add_log(message)
