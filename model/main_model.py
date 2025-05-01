from fileWatcher import FileWatcher
from eventHandler import EventHandler

if __name__ == "__main__":
    watcher = FileWatcher('/Users/ndly/Desktop/TCSS/TCSS 360/FileWatcher/testFileToWatch', MyEventHandler())
    watcher.run()