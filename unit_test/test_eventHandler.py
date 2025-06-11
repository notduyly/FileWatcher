import unittest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock, call
import sys
from watchdog.events import FileSystemEvent, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent

# Add the parent directory to the path so we can import from model
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model.eventHandler import MyEventHandler

class TestMyEventHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_log_callback = Mock()
        self.test_file_path = "/test/path/file.txt"
        
    def create_mock_event(self, event_type, src_path):
        """Helper method to create mock file system events."""
        if event_type == 'modified':
            return FileModifiedEvent(src_path)
        elif event_type == 'created':
            return FileCreatedEvent(src_path)
        elif event_type == 'deleted':
            return FileDeletedEvent(src_path)
        else:
            # Generic event for testing
            mock_event = Mock()
            mock_event.src_path = src_path
            return mock_event
    
    def test_init_default_parameters(self):
        """Test MyEventHandler initialization with default parameters."""
        handler = MyEventHandler()
        self.assertIsNone(handler._MyEventHandler__myLogToTextbox)
        self.assertEqual(handler._MyEventHandler__myExtensionFilter, '')
    
    def test_init_with_log_callback(self):
        """Test MyEventHandler initialization with log callback."""
        handler = MyEventHandler(self.mock_log_callback)
        self.assertEqual(handler._MyEventHandler__myLogToTextbox, self.mock_log_callback)
        self.assertEqual(handler._MyEventHandler__myExtensionFilter, '')
    
    def test_set_extension_filter(self):
        """Test setting file extension filter."""
        handler = MyEventHandler()
        
        handler.set_extension_filter('.txt')
        self.assertEqual(handler._MyEventHandler__myExtensionFilter, '.txt')
        
        handler.set_extension_filter('.png')
        self.assertEqual(handler._MyEventHandler__myExtensionFilter, '.png')
    
    @patch('model.eventHandler.FileSystemEventHandler.on_modified')
    def test_on_modified_with_callback(self, mock_super_on_modified):
        """Test on_modified method with log callback."""
        handler = MyEventHandler(self.mock_log_callback)
        mock_event = self.create_mock_event('modified', self.test_file_path)
        
        result = handler.on_modified(mock_event)
        
        self.mock_log_callback.assert_called_once_with(f'Modified: {self.test_file_path}')
        mock_super_on_modified.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.on_modified')
    def test_on_modified_without_callback(self, mock_super_on_modified):
        """Test on_modified method without log callback."""
        handler = MyEventHandler()
        mock_event = self.create_mock_event('modified', self.test_file_path)
        
        result = handler.on_modified(mock_event)
        
        mock_super_on_modified.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.on_created')
    def test_on_created_with_callback(self, mock_super_on_created):
        """Test on_created method with log callback."""
        handler = MyEventHandler(self.mock_log_callback)
        mock_event = self.create_mock_event('created', self.test_file_path)
        
        result = handler.on_created(mock_event)
        
        self.mock_log_callback.assert_called_once_with(f'Created: {self.test_file_path}')
        mock_super_on_created.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.on_created')
    def test_on_created_without_callback(self, mock_super_on_created):
        """Test on_created method without log callback."""
        handler = MyEventHandler()
        mock_event = self.create_mock_event('created', self.test_file_path)
        
        result = handler.on_created(mock_event)
        
        mock_super_on_created.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.on_deleted')
    def test_on_deleted_with_callback(self, mock_super_on_deleted):
        """Test on_deleted method with log callback."""
        handler = MyEventHandler(self.mock_log_callback)
        mock_event = self.create_mock_event('deleted', self.test_file_path)
        
        result = handler.on_deleted(mock_event)
        
        self.mock_log_callback.assert_called_once_with(f'Deleted: {self.test_file_path}')
        mock_super_on_deleted.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.on_deleted')
    def test_on_deleted_without_callback(self, mock_super_on_deleted):
        """Test on_deleted method without log callback."""
        handler = MyEventHandler()
        mock_event = self.create_mock_event('deleted', self.test_file_path)
        
        result = handler.on_deleted(mock_event)
        
        mock_super_on_deleted.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.dispatch')
    def test_dispatch_empty_filter(self, mock_super_dispatch):
        """Test dispatch method with empty extension filter."""
        handler = MyEventHandler()
        handler.set_extension_filter('')
        mock_event = self.create_mock_event('modified', '/test/file.txt')
        
        result = handler.dispatch(mock_event)
        
        mock_super_dispatch.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.dispatch')
    def test_dispatch_none_filter(self, mock_super_dispatch):
        """Test dispatch method with 'None' string filter."""
        handler = MyEventHandler()
        handler.set_extension_filter('None')
        mock_event = self.create_mock_event('modified', '/test/file.txt')
        
        result = handler.dispatch(mock_event)
        
        mock_super_dispatch.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.dispatch')
    def test_dispatch_with_matching_filter(self, mock_super_dispatch):
        """Test dispatch method with matching extension filter."""
        handler = MyEventHandler()
        handler.set_extension_filter('.txt')
        mock_event = self.create_mock_event('modified', '/test/file.txt')
        
        result = handler.dispatch(mock_event)
        
        mock_super_dispatch.assert_called_once_with(mock_event)
    
    @patch('model.eventHandler.FileSystemEventHandler.dispatch')
    def test_dispatch_with_non_matching_filter(self, mock_super_dispatch):
        """Test dispatch method with non-matching extension filter."""
        handler = MyEventHandler()
        handler.set_extension_filter('.txt')
        mock_event = self.create_mock_event('modified', '/test/file.png')
        
        result = handler.dispatch(mock_event)
        
        mock_super_dispatch.assert_not_called()
    
    def test_multiple_extension_filters(self):
        """Test setting multiple extension filters in sequence."""
        handler = MyEventHandler()
        
        handler.set_extension_filter('.txt')
        self.assertEqual(handler._MyEventHandler__myExtensionFilter, '.txt')
        
        handler.set_extension_filter('.png')
        self.assertEqual(handler._MyEventHandler__myExtensionFilter, '.png')
        
    
    def test_integration_all_event_types(self):
        """Test integration of all event types with logging."""
        log_messages = []
        
        def capture_log(message):
            log_messages.append(message)
        
        handler = MyEventHandler(capture_log)
        
        # Test all event types
        events = [
            ('modified', '/test/file1.txt'),
            ('created', '/test/file2.txt'),
            ('deleted', '/test/file3.txt'),
        ]
        
        with patch('model.eventHandler.FileSystemEventHandler.on_modified'), \
            patch('model.eventHandler.FileSystemEventHandler.on_created'), \
            patch('model.eventHandler.FileSystemEventHandler.on_deleted'):
            
            for event_type, path in events:
                mock_event = self.create_mock_event(event_type, path)
                if event_type == 'modified':
                    handler.on_modified(mock_event)
                elif event_type == 'created':
                    handler.on_created(mock_event)
                elif event_type == 'deleted':
                    handler.on_deleted(mock_event)
        
        expected_messages = [
            'Modified: /test/file1.txt',
            'Created: /test/file2.txt',
            'Deleted: /test/file3.txt',
        ]
        
        self.assertEqual(log_messages, expected_messages)


if __name__ == '__main__':
    unittest.main()