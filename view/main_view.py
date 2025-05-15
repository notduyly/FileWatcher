import tkinter as tk
import sys
import os

from view.menubar import MenuBar
from .setup_window import setupWindow

class FileWatcherGUI:
    def __init__(self, root, controller):
        self.controller = controller
        self.window = setupWindow(root, controller)
        self.menubar = MenuBar(root, controller)

        root.config(menu=self.menubar.get_menubar())
        controller.set_view(self)

    def add_log(self, message):
        self.window.add_log(message)
