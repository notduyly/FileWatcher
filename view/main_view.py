from view.menubar import MenuBar
from .setup_window import SetupWindow

class FileWatcherGUI:
    """
    Main GUI class that coordinates the application interface.
    
    Attributes:
        __myRoot: The root Tkinter window instance.
        __myController: The main controller instance.
        __myWindow: The main setup window component.
        __myMenubar: The application menu bar component.
    """
    
    def __init__(self, theRoot, theController):
        """
        Initialize the FileWatcherGUI with root window and controller.
        
        Args:
            theRoot: The root Tkinter window instance.
            theController: The main controller.
        """
        self.__myRoot = theRoot
        self.__myController = theController
        self.__myWindow = SetupWindow(theRoot, theController)
        self.__myMenubar = MenuBar(theRoot, theController)

        self.__myRoot.config(menu=self.__myMenubar.get_menubar())
        self.__myController.set_view(self)

    def add_log(self, theMessage):
        """
        Adds a log message to the main window display.
        
        Args:
            theMessage: The log message to display in the UI.
        """
        self.__myWindow.add_log(theMessage)

    def update_directory_display(self, theDirectory):
        """
        Updates the directory display in the main window.
        
        Args:
            theDirectory: The directory path to display in the UI.
        """
        self.__myWindow.update_directory_display(theDirectory)
    
    def get_root(self):
        """
        Gets the root Tkinter window instance.
        
        Returns:
            The root Tkinter window instance used by this GUI.
        """
        return self.__myRoot
    
    def save_to_database(self):
        """
        Triggers the save to database operation.
        """
        self.__myWindow._save_to_database()

    def get_window(self):
        """
        Gets the setup window instance.
        
        Returns:
            The SetupWindow instance.
        """
        return self.__myWindow
