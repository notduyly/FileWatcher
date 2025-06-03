from view.menubar import MenuBar
from .setup_window import SetupWindow

class FileWatcherGUI:
    def __init__(self, theRoot, theController):
        self.__myRoot = theRoot
        self.__myController = theController
        self.__myWindow = SetupWindow(theRoot, theController)
        self.__myMenubar = MenuBar(theRoot, theController)

        self.__myRoot.config(menu=self.__myMenubar.get_menubar())
        self.__myController.set_view(self)

    def add_log(self, theMessage):
        self.__myWindow.add_log(theMessage)

    def update_directory_display(self, theDirectory):
        self.__myWindow.update_directory_display(theDirectory)
    
    def get_root(self):
        return self.__myRoot