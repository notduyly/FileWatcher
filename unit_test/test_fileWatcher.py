import unittest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
import time
from watchdog.events import LoggingEventHandler
import sys
import shutil

# Add the parent directory to the path so we can import from model
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model.fileWatcher import FileWatcher

class TestFileWatcher(unittest.TestCase):
  
  def setUp(self):
    """Set up test fixtures before each test method."""
    self.test_path = tempfile.mkdtemp()
    self.mock_handler = Mock()
    
  def tearDown(self):
    """Clean up after each test method."""
    shutil.rmtree(self.test_path)
  
  def test_init_default_parameters(self):
    """Test FileWatcher initialization with default parameters."""
    watcher = FileWatcher(self.test_path)
    self.assertEqual(watcher._FileWatcher__myPath, self.test_path)
    self.assertIsInstance(watcher._FileWatcher__myEventHandler, LoggingEventHandler)
    self.assertTrue(watcher._FileWatcher__myRecursive)
    self.assertIsNone(watcher._FileWatcher__myObserver)
  
  def test_init_custom_parameters(self):
    """Test FileWatcher initialization with custom parameters."""
    watcher = FileWatcher(self.test_path, self.mock_handler, False)
    self.assertEqual(watcher._FileWatcher__myPath, self.test_path)
    self.assertEqual(watcher._FileWatcher__myEventHandler, self.mock_handler)
    self.assertFalse(watcher._FileWatcher__myRecursive)
    self.assertIsNone(watcher._FileWatcher__myObserver)
  
  @patch('model.fileWatcher.Observer')
  def test_start(self, mock_observer_class):
    """Test starting the file watcher."""
    mock_observer = Mock()
    mock_observer_class.return_value = mock_observer
    
    watcher = FileWatcher(self.test_path, self.mock_handler)
    watcher.start()
    
    mock_observer_class.assert_called_once()
    mock_observer.schedule.assert_called_once_with(
      self.mock_handler, self.test_path, recursive=True
    )
    mock_observer.start.assert_called_once()
    self.assertEqual(watcher._FileWatcher__myObserver, mock_observer)
  
  def test_stop_with_observer(self):
    """Test stopping the file watcher when observer exists."""
    watcher = FileWatcher(self.test_path)
    mock_observer = Mock()
    watcher._FileWatcher__myObserver = mock_observer
    
    watcher.stop()
    
    mock_observer.stop.assert_called_once()
    mock_observer.join.assert_called_once()
  
  def test_stop_without_observer(self):
    """Test stopping the file watcher when no observer exists."""
    watcher = FileWatcher(self.test_path)
    # Should not raise an exception
    watcher.stop()
  
  @patch('model.fileWatcher.time.sleep')
  @patch('model.fileWatcher.Observer')
  def test_run_keyboard_interrupt(self, mock_observer_class, mock_sleep):
    """Test run method with KeyboardInterrupt."""
    mock_observer = Mock()
    mock_observer_class.return_value = mock_observer
    mock_sleep.side_effect = KeyboardInterrupt()
    
    watcher = FileWatcher(self.test_path)
    watcher.run()
    
    mock_observer.start.assert_called_once()
    mock_observer.stop.assert_called_once()
    mock_observer.join.assert_called_once()
  
  @patch('model.fileWatcher.Observer')
  def test_start_stop_integration(self, mock_observer_class):
    """Test integration of start and stop methods."""
    mock_observer = Mock()
    mock_observer_class.return_value = mock_observer
    
    watcher = FileWatcher(self.test_path, self.mock_handler, False)
    
    # Start the watcher
    watcher.start()
    self.assertIsNotNone(watcher._FileWatcher__myObserver)
    
    # Stop the watcher
    watcher.stop()
    mock_observer.stop.assert_called_once()
    mock_observer.join.assert_called_once()


if __name__ == '__main__':
  unittest.main()