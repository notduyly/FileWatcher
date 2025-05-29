import logging
from watchdog.events import FileSystemEventHandler
from .db_handler import insert_event

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, logToTextbox=None):
        super().__init__()
        self.__myLogToTextbox = logToTextbox
        self.__myExtensionFilter = ''

    def set_extension_filter(self, theExtension):
        self.__myExtensionFilter = theExtension

    def on_modified(self, theEvent):
        msg = f'Modified: {theEvent.src_path}'
        if self.__myLogToTextbox:
            self.__myLogToTextbox(msg)
        # 데이터베이스에 이벤트 저장
        insert_event('modified', theEvent.src_path)
        return super().on_modified(theEvent)
    
    def on_created(self, theEvent):
        msg = f'Created: {theEvent.src_path}'
        if self.__myLogToTextbox:
            self.__myLogToTextbox(msg)
        # 데이터베이스에 이벤트 저장
        insert_event('created', theEvent.src_path)
        return super().on_created(theEvent)
    
    def on_deleted(self, theEvent):
        msg = f'Deleted: {theEvent.src_path}'
        if self.__myLogToTextbox:
            self.__myLogToTextbox(msg)
        # 데이터베이스에 이벤트 저장
        insert_event('deleted', theEvent.src_path)
        return super().on_deleted(theEvent)

    def dispatch(self, theEvent):
        # Log the event if it matches the extension
        if self.__myExtensionFilter and self.__myExtensionFilter != 'None':
            if theEvent.src_path.lower().endswith(self.__myExtensionFilter.lower()):
                return super().dispatch(theEvent)
        else: 
            # Log all events if there are no extension
            return super().dispatch(theEvent)
