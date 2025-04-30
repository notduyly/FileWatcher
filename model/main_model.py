from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print('File created: ', event.src_path)
        return super().on_created(event)

    def on_modified(self, event):
        print('File modified: ', event.src_path)
        return super().on_modified(event)

    def on_deleted(self, event):
        print('File deleted: ', event.src_path)
        return super().on_deleted(event)

    def on_moved(self, event):
        print('File moved: ', event.src_path)
        return super().on_moved(event)

def main(filePath):
    path = filePath
    observer = Observer()
    handler = MyHandler()
    observer.schedule(handler, path, recursive=True)
    observer.start()

    while True:
        cmd = input('> ')
        if cmd == 'q': break
    
    observer.stop()
    observer.join()

if __name__ == '__main__':
    main() 
