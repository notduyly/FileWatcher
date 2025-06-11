import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, mock_open, MagicMock, call
from datetime import datetime
import csv

# Add the parent directory to the path so we can import from model
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model.db_handler import (
    insert_event, delete_event, reset_database, fetch_all_events,
    fetch_event_by_type, fetch_event_by_extension, fetch_event_by_after_date,
    get_event_count, get_event_by_id, query_events, get_unique_extensions,
    save_multiple_events, format_event_for_display, export_events_to_csv
)

class TestDbHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_conn = Mock()
        self.mock_cursor = Mock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_conn.__enter__ = Mock(return_value=self.mock_conn)
        self.mock_conn.__exit__ = Mock(return_value=None)
        
        self.test_event = "created"
        self.test_path = "/test/path/file.txt"
        self.test_timestamp = "2023-06-10 12:00:00"
        
        # Sample event data for testing
        self.sample_events = [
            (1, "test.txt", "/path/test.txt", ".txt", "created", "2023-06-10 12:00:00", 1024, "testuser"),
            (2, "doc.pdf", "/path/doc.pdf", ".pdf", "modified", "2023-06-10 13:00:00", 2048, "testuser"),
            (3, "image.png", "/path/image.png", ".png", "deleted", "2023-06-10 14:00:00", None, "testuser")
        ]

    @patch('model.db_handler.get_connection')
    @patch('model.db_handler.getpass.getuser')
    @patch('model.db_handler.os.path.getsize')
    @patch('model.db_handler.os.path.isfile')
    @patch('model.db_handler.os.path.abspath')
    @patch('model.db_handler.os.path.basename')
    @patch('model.db_handler.os.path.splitext')
    @patch('model.db_handler.datetime')
    def test_insert_event_success(self, mock_datetime, mock_splitext, mock_basename, 
                                 mock_abspath, mock_isfile, mock_getsize, 
                                 mock_getuser, mock_get_conn):
        """Test successful event insertion."""
        # Setup mocks
        mock_get_conn.return_value = self.mock_conn
        mock_datetime.now.return_value.strftime.return_value = self.test_timestamp
        mock_abspath.return_value = "/absolute/path/file.txt"
        mock_basename.return_value = "file.txt"
        mock_splitext.return_value = ("file", ".txt")
        mock_isfile.return_value = True
        mock_getsize.return_value = 1024
        mock_getuser.return_value = "testuser"
        
        # Test
        insert_event(self.test_event, self.test_path)
        
        # Assertions
        self.mock_conn.execute.assert_called_once()
        call_args = self.mock_conn.execute.call_args
        self.assertIn("INSERT INTO events", call_args[0][0])
        self.assertEqual(call_args[0][1][0], "file.txt")  # filename
        self.assertEqual(call_args[0][1][3], self.test_event)  # event type
    
    @patch('model.db_handler.get_connection')
    def test_delete_event_success(self, mock_get_conn):
        """Test successful event deletion."""
        mock_get_conn.return_value = self.mock_conn
        test_id = 123
        
        # Test
        delete_event(test_id)
        
        # Assertions
        self.mock_conn.execute.assert_called_once_with(
            'DELETE FROM events WHERE id = ?', (test_id,)
        )
    
    @patch('model.db_handler.get_connection')  
    @patch('model.database._init_db')
    def test_reset_database_success(self, mock_init_db, mock_get_conn):
        """Test successful database reset."""
        mock_get_conn.return_value = self.mock_conn
        
        # Test
        result = reset_database()
        
        # Assertions
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once_with('DROP TABLE IF EXISTS events')
        mock_init_db.assert_called_once()
    
    @patch('model.db_handler.get_connection')
    @patch('builtins.print')
    def test_reset_database_exception(self, mock_print, mock_get_conn):
        """Test reset_database when exception occurs."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = Exception("Database error")
        
        result = reset_database()
        
        self.assertFalse(result)
        mock_print.assert_called_with("Error resetting database: Database error")
    
    @patch('model.db_handler.get_connection')
    def test_fetch_all_events_success(self, mock_get_conn):
        """Test successful fetch of all events."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = self.sample_events
        
        result = fetch_all_events()
        
        self.assertEqual(result, self.sample_events)
        self.mock_cursor.execute.assert_called_once_with('SELECT * FROM events')
    
    @patch('model.db_handler.get_connection')
    def test_fetch_event_by_type_all(self, mock_get_conn):
        """Test fetch_event_by_type with 'All' parameter."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = self.sample_events
        
        result = fetch_event_by_type('All')
        
        self.assertEqual(result, self.sample_events)
        self.mock_cursor.execute.assert_called_once()
        self.assertIn('ORDER BY event_timestamp DESC', 
                      self.mock_cursor.execute.call_args[0][0])
    
    @patch('model.db_handler.get_connection')
    def test_fetch_event_by_type_specific(self, mock_get_conn):
        """Test fetch_event_by_type with specific event type."""
        mock_get_conn.return_value = self.mock_conn
        filtered_events = [self.sample_events[0]]  # Only 'created' events
        self.mock_cursor.fetchall.return_value = filtered_events
        
        result = fetch_event_by_type('created')
        
        self.assertEqual(result, filtered_events)
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args
        self.assertIn('WHERE event = ?', call_args[0][0])
        self.assertEqual(call_args[0][1], ('created',))
    
    @patch('model.db_handler.get_connection')
    def test_fetch_event_by_extension_all(self, mock_get_conn):
        """Test fetch_event_by_extension with 'All' parameter."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = self.sample_events
        
        result = fetch_event_by_extension('All')
        
        self.assertEqual(result, self.sample_events)
    
    @patch('model.db_handler.get_connection')
    def test_fetch_event_by_extension_specific(self, mock_get_conn):
        """Test fetch_event_by_extension with specific extension."""
        mock_get_conn.return_value = self.mock_conn
        filtered_events = [self.sample_events[0]]  # Only .txt files
        self.mock_cursor.fetchall.return_value = filtered_events
        
        result = fetch_event_by_extension('.txt')
        
        self.assertEqual(result, filtered_events)
        call_args = self.mock_cursor.execute.call_args
        self.assertIn('WHERE file_extension = ?', call_args[0][0])
        self.assertEqual(call_args[0][1], ('.txt',))
    
    @patch('model.db_handler.get_connection')
    def test_fetch_event_by_after_date_options(self, mock_get_conn):
        """Test fetch_event_by_after_date with different date options."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = self.sample_events
        
        date_options = ['All', 'Today', 'Last 7 days', 'Last 30 days']
        
        for option in date_options:
            with self.subTest(option=option):
                self.mock_cursor.reset_mock()
                result = fetch_event_by_after_date(option)
                
                self.assertEqual(result, self.sample_events)
                self.mock_cursor.execute.assert_called_once()
                
                if option != 'All':
                    query = self.mock_cursor.execute.call_args[0][0]
                    self.assertIn('WHERE', query)
    
    @patch('model.db_handler.get_connection')
    def test_get_event_count_success(self, mock_get_conn):
        """Test successful event count retrieval."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = (42,)
        
        result = get_event_count()
        
        self.assertEqual(result, 42)
        self.mock_cursor.execute.assert_called_once_with('SELECT COUNT(*) FROM events')
        
    @patch('model.db_handler.get_connection')
    def test_get_event_by_id_success(self, mock_get_conn):
        """Test successful event retrieval by ID."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = self.sample_events[0]
        
        result = get_event_by_id(1)
        
        self.assertEqual(result, self.sample_events[0])
        self.mock_cursor.execute.assert_called_once_with(
            'SELECT * FROM events WHERE id = ?', (1,)
        )
    
    @patch('model.db_handler.get_connection')
    def test_get_event_by_id_not_found(self, mock_get_conn):
        """Test get_event_by_id when event not found."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = None
        
        result = get_event_by_id(999)
        
        self.assertIsNone(result)
    
    @patch('model.db_handler.get_connection')
    @patch('builtins.print')
    def test_query_events_with_filters(self, mock_print, mock_get_conn):
        """Test query_events with various filters."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = self.sample_events
        
        filters = {
            'event_type': 'created',
            'extension': '.txt',
            'date_range': 'Today'
        }
        
        result = query_events(filters)
        
        self.assertEqual(result, self.sample_events)
        self.mock_cursor.execute.assert_called_once()
        
        # Check that query contains expected filters
        query = self.mock_cursor.execute.call_args[0][0]
        params = self.mock_cursor.execute.call_args[0][1]
        
        self.assertIn('AND event LIKE ?', query)
        self.assertIn('AND file_extension = ?', query)
        self.assertIn("AND DATE(event_timestamp) = DATE('now')", query)
        self.assertIn('%created%', params)
        self.assertIn('.txt', params)
    
    @patch('model.db_handler.get_connection')
    @patch('builtins.print')
    def test_query_events_no_filters(self, mock_print, mock_get_conn):
        """Test query_events without filters."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = self.sample_events
        
        result = query_events(None)
        
        self.assertEqual(result, self.sample_events)
        query = self.mock_cursor.execute.call_args[0][0]
        self.assertIn('WHERE 1=1', query)
        self.assertIn('ORDER BY event_timestamp DESC', query)
    
    @patch('model.db_handler.get_connection')
    @patch('builtins.print')
    def test_query_events_exception(self, mock_print, mock_get_conn):
        """Test query_events when exception occurs."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = Exception("Query error")
        
        result = query_events({'event_type': 'created'})
        
        self.assertEqual(result, [])
        mock_print.assert_called_with("Database error: Query error")
    
    @patch('model.db_handler.get_connection')
    def test_get_unique_extensions_success(self, mock_get_conn):
        """Test successful retrieval of unique extensions."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [('.txt',), ('.pdf',), ('.png',)]
        
        result = get_unique_extensions()
        
        expected = ['All', '.txt', '.pdf', '.png']
        self.assertEqual(result, expected)
        
        query = self.mock_cursor.execute.call_args[0][0]
        self.assertIn('SELECT DISTINCT file_extension', query)
        self.assertIn('WHERE file_extension != ""', query)
    
    @patch('model.db_handler.get_connection')
    def test_save_multiple_events_empty_list(self, mock_get_conn):
        """Test save_multiple_events with empty event list."""
        result = save_multiple_events([])
        
        self.assertFalse(result)
        mock_get_conn.assert_not_called()
    
    @patch('model.db_handler.get_connection')
    @patch('builtins.print')
    def test_save_multiple_events_exception(self, mock_print, mock_get_conn):
        """Test save_multiple_events when exception occurs."""
        mock_get_conn.return_value = self.mock_conn
        self.mock_conn.cursor.side_effect = Exception("Database error")
        
        events = [{'filepath': '/test/file.txt', 'event_type': 'created'}]
        result = save_multiple_events(events)
        
        self.assertFalse(result)
        mock_print.assert_called_with("Error saving events to database: Database error")
    
    @patch('model.db_handler.os.path.basename')
    @patch('model.db_handler.os.path.splitext')
    @patch('model.db_handler.os.path.relpath')
    def test_format_event_for_display(self, mock_relpath, mock_splitext, mock_basename):
        """Test event formatting for display."""
        mock_basename.return_value = "test.txt"
        mock_splitext.return_value = ("test", ".txt")
        mock_relpath.return_value = "relative/path/test.txt"
        
        event = self.sample_events[0]
        result = format_event_for_display(event)
        
        expected = ("test.txt", ".txt", "relative/path/test.txt", "created", "2023-06-10 12:00:00")
        self.assertEqual(result, expected)
    
    @patch('model.db_handler.os.path.basename')
    @patch('model.db_handler.os.path.splitext')
    @patch('model.db_handler.os.path.relpath')
    def test_format_event_for_display_no_extension(self, mock_relpath, mock_splitext, mock_basename):
        """Test event formatting when file has no extension."""
        mock_basename.return_value = "testfile"
        mock_splitext.return_value = ("testfile", "")
        mock_relpath.return_value = "relative/path/testfile"
        
        event = (1, "testfile", "/path/testfile", "", "created", "2023-06-10 12:00:00", 1024, "user")
        result = format_event_for_display(event)
        
        expected = ("testfile", "(none)", "relative/path/testfile", "created", "2023-06-10 12:00:00")
        self.assertEqual(result, expected)
    
    @patch('model.db_handler.format_event_for_display')
    def test_export_events_to_csv_success(self, mock_format):
        """Test successful CSV export."""
        mock_format.side_effect = [
            ("file1.txt", ".txt", "path1", "created", "2023-06-10 12:00:00"),
            ("file2.pdf", ".pdf", "path2", "modified", "2023-06-10 13:00:00")
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('model.db_handler.csv.writer') as mock_writer_class:
                mock_writer = Mock()
                mock_writer_class.return_value = mock_writer
                
                result = export_events_to_csv("/test/export.csv", self.sample_events[:2])
                
                self.assertTrue(result)
                mock_file.assert_called_once_with("/test/export.csv", 'w', newline='', encoding='utf-8')
                mock_writer.writerow.assert_any_call(['Filename', 'Extension', 'Path', 'Event', 'Timestamp'])
                self.assertEqual(mock_writer.writerow.call_count, 3)  # Header + 2 data rows
    
    @patch('builtins.print')
    def test_export_events_to_csv_exception(self, mock_print):
        """Test CSV export when exception occurs."""
        with patch('builtins.open', side_effect=IOError("File error")):
            result = export_events_to_csv("/invalid/path.csv", self.sample_events)
            
            self.assertFalse(result)
            mock_print.assert_called_with("Error exporting to CSV: File error")


if __name__ == '__main__':
    unittest.main()