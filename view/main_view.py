import tkinter as tk
import sys
import os
from .setup_window import setupWindow

class FileWatcherGUI:
    def __init__(self, root, controller):
        self.controller = controller
        
        self.window = setupWindow(root, controller)
        controller.set_view(self)

    def add_log(self, message):
        self.window.add_log(message)
