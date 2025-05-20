from view.menubar import MenuBar
from .setup_window import setupWindow

class FileWatcherGUI:
    def __init__(self, theRoot, theController):
        self.myController = theController
        self.myWindow = setupWindow(theRoot, theController)
        self.myMenubar = MenuBar(theRoot)

        theRoot.config(menu=self.myMenubar.get_menubar())
        theController.set_view(self)

    def add_log(self, theMessage):
        self.myWindow.add_log(theMessage)
