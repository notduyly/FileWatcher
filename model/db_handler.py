import sqlite3
import csv
import os
from datetime import datetime
import getpass
from .database import get_connection

def init_event_table():
    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_extension TEXT NOT NULL,
                    event TEXT NOT NULL,
                    event_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    file_size INTEGER,
                    is_directory BOOLEAN,
                    user TEXT
                )
            ''')

def insert_event(event_type, file_path, is_directory=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]
    file_size = os.path.getsize(file_path) if not is_directory and os.path.isfile(file_path) else None
    user = getpass.getuser()

    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            conn.execute("""
                INSERT INTO events (
                    filename, file_path, file_extension, event,
                    event_timestamp, file_size, is_directory, user
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                file_name, file_path, file_extension, event_type,
                timestamp, file_size, is_directory, user
            ))

def delete_event(theEventId: int):
    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            conn.execute('DELETE FROM events WHERE id = ?', (theEventId,))

def reset_db():
    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            conn.execute('DROP TABLE IF EXISTS events')

def fetch_all_events():
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        return cursor.fetchall()

def fetch_event_by_type(event_type='All'):
    """Fetch events filtered by event type"""
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        
        if event_type == 'All':
            cursor.execute('''
                SELECT * FROM events 
                ORDER BY event_timestamp DESC
            ''')
        else:
            cursor.execute('''
                SELECT * FROM events 
                WHERE event = ? 
                ORDER BY event_timestamp DESC
            ''', (event_type,))
            
        return cursor.fetchall()

def fetch_event_by_extension(extension='All'):
    """Fetch events filtered by file extension"""
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        
        if extension == 'All':
            cursor.execute('''
                SELECT * FROM events 
                ORDER BY event_timestamp DESC
            ''')
        else:
            cursor.execute('''
                SELECT * FROM events 
                WHERE file_extension = ? 
                ORDER BY event_timestamp DESC
            ''', (extension,))
            
        return cursor.fetchall()

def fetch_event_by_after_date(date_range='All'):
    """Fetch events filtered by date range"""
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        
        if date_range == 'All':
            cursor.execute('SELECT * FROM events ORDER BY event_timestamp DESC')
        elif date_range == 'Today':
            cursor.execute('SELECT * FROM events WHERE DATE(event_timestamp) = DATE("now") ORDER BY event_timestamp DESC')
        elif date_range == 'Last 7 days':
            cursor.execute('SELECT * FROM events WHERE event_timestamp >= datetime("now", "-7 days") ORDER BY event_timestamp DESC')
        elif date_range == 'Last 30 days':
            cursor.execute('SELECT * FROM events WHERE event_timestamp >= datetime("now", "-30 days") ORDER BY event_timestamp DESC')
        
        return cursor.fetchall()

def export_to_csv(theFilename: str):
    events = fetch_all_events()
    with open(theFilename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'ID', 'Filename', 'File Path', 'File Extension',
            'Event', 'Event Timestamp', 'File Size', 'Is Directory', 'User'
        ])
        writer.writerows(events)
    print(f"✅ Data exported to {theFilename} successfully.")

def get_event_count():
    with get_connection() as conn:
        if conn is None:
            return 0
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM events')
        return cursor.fetchone()[0]

def get_event_by_id(theEventId: int):
    with get_connection() as conn:
        if conn is None:
            return None
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE id = ?', (theEventId,))
        return cursor.fetchone()
