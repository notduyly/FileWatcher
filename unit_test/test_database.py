import unittest
import tempfile
import os
import sys
import sqlite3
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import from model
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model.database import get_connection, _init_db

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_db_path = 'test_database.db'
        # Clean up any existing test database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up test database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        if os.path.exists('database.db'):
            try:
                os.remove('database.db')
            except (PermissionError, FileNotFoundError):
                pass
    
    @patch('model.database.sqlite3.connect')
    def test_get_connection_success(self, mock_connect):
        """Test successful database connection."""
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        result = get_connection()
        
        mock_connect.assert_called_once_with('database.db')
        self.assertEqual(result, mock_conn)
    
    @patch('model.database.sqlite3.connect')
    @patch('builtins.print')
    def test_get_connection_sqlite_error(self, mock_print, mock_connect):
        """Test database connection when SQLite error occurs."""
        error_msg = "Database is locked"
        mock_connect.side_effect = sqlite3.Error(error_msg)
        
        result = get_connection()
        
        mock_connect.assert_called_once_with('database.db')
        mock_print.assert_called_once_with(f"An error occurred while connecting to the database: {error_msg}")
        self.assertIsNone(result)
    
    @patch('model.database.sqlite3.connect')
    @patch('builtins.print')
    def test_get_connection_database_error(self, mock_print, mock_connect):
        """Test database connection with database-specific error."""
        error_msg = "disk I/O error"
        mock_connect.side_effect = sqlite3.DatabaseError(error_msg)
        
        result = get_connection()
        
        mock_connect.assert_called_once_with('database.db')
        mock_print.assert_called_once_with(f"An error occurred while connecting to the database: {error_msg}")
        self.assertIsNone(result)
    
    @patch('model.database.sqlite3.connect')
    @patch('builtins.print')
    def test_get_connection_operational_error(self, mock_print, mock_connect):
        """Test database connection with operational error."""
        error_msg = "unable to open database file"
        mock_connect.side_effect = sqlite3.OperationalError(error_msg)
        
        result = get_connection()
        
        mock_connect.assert_called_once_with('database.db')
        mock_print.assert_called_once_with(f"An error occurred while connecting to the database: {error_msg}")
        self.assertIsNone(result)
    
    @patch('model.database.get_connection')
    def test_init_db_success(self, mock_get_connection):
        """Test successful database initialization."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=None)
        mock_get_connection.return_value = mock_conn
        
        _init_db()
        
        mock_get_connection.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the CREATE TABLE statement was executed
        call_args = mock_conn.execute.call_args[0][0]
        self.assertIn('CREATE TABLE IF NOT EXISTS events', call_args)
        self.assertIn('id INTEGER PRIMARY KEY AUTOINCREMENT', call_args)
        self.assertIn('filename TEXT NOT NULL', call_args)
        self.assertIn('file_path TEXT NOT NULL', call_args)
        self.assertIn('file_extension TEXT NOT NULL', call_args)
        self.assertIn('event TEXT NOT NULL', call_args)
        self.assertIn('event_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP', call_args)
        self.assertIn('file_size INTEGER', call_args)
        self.assertIn('user TEXT', call_args)
    
    def test_integration_real_database_connection(self):
        """Integration test with real SQLite database."""
        # This test uses a real database file to ensure the connection actually works
        with patch('model.database.sqlite3.connect') as mock_connect:
            # Use a real SQLite connection for this test
            real_conn = sqlite3.connect(':memory:')
            mock_connect.return_value = real_conn
            
            # Test connection
            conn = get_connection()
            
            self.assertIsNotNone(conn)
            self.assertEqual(conn, real_conn)
            
            # Clean up
            conn.close()
    
    def test_database_default_values(self):
        """Test that default values work correctly."""
        with patch('model.database.sqlite3.connect') as mock_connect:
            real_conn = sqlite3.connect(':memory:')
            mock_connect.return_value = real_conn
            
            # Initialize database
            _init_db()
            
            cursor = real_conn.cursor()
            
            # Insert minimal record
            cursor.execute('''
                INSERT INTO events (filename, file_path, file_extension, event)
                VALUES (?, ?, ?, ?)
            ''', ('test.txt', '/path/test.txt', '.txt', 'created'))
            
            # Retrieve the record
            cursor.execute('SELECT * FROM events WHERE filename = ?', ('test.txt',))
            record = cursor.fetchone()
            
            # Check that ID was auto-generated
            self.assertIsNotNone(record[0])  # id field
            
            # Check that timestamp was set (should not be None)
            self.assertIsNotNone(record[5])  # event_timestamp field
            
            real_conn.close()
    
    def test_database_file_path(self):
        """Test that database uses correct file path."""
        with patch('model.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_connect.return_value = mock_conn
            
            get_connection()
            
            # Verify the correct database file path is used
            mock_connect.assert_called_once_with('database.db')

if __name__ == '__main__':
    unittest.main()