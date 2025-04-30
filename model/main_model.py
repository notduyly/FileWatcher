# import the modules
from fileWatcher import FileWatcher
from eventHandler import MyEventHandler

if __name__ == "__main__":
    watcher = FileWatcher('/Users/ndly/Desktop/TCSS/TCSS 360/FileWatcher/testFileToWatch', MyEventHandler())
    watcher.run()