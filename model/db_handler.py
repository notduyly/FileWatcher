import sqlite3
import csv
import os
from datetime import datetime
import getpass
from .database import get_connection

def init_event_table():
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_extension TEXT NOT NULL,
            event_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_size INTEGER NOT NULL,
            event TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
# def insert_event(theEventType: str, theFilePath: str, theFileSize: int):
#     """
#     Insert a file event with additional metadata
#     """
#     conn = get_connection()
#     if conn is None:
#         return
    
#     file_extension = theFilename.split('.')[-1] if '.' in theFilename else ''
    
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO events (filename, file_extension, file_size, event)
#         VALUES (?, ?, ?, ?)
#     ''', (theFilename, file_extension, theFileSize, theEvent))
    
#     conn.commit()
#     conn.close()
    
def insert_event(event_type, file_path, is_directory=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]
    
    file_size = os.path.getsize(file_path) if not is_directory and os.path.isfile(file_path) else None
    
    user = getpass.getuser()

    conn = sqlite3.connect("file_events.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (
            timestamp, event_type, file_path, file_name,
            file_extension, file_size, is_directory, user
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, event_type, file_path, file_name,
        file_extension, file_size, is_directory, user
    ))
    conn.commit()
    conn.close()
    
def delete_event(theEventId: int):
    """
    Deletes an event from the database by its ID.
    """
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM events WHERE id = ?
    ''', (theEventId,))
    conn.commit()
    conn.close()
    
def reset_db():
    """
    Resets the database by dropping all tables.
    """
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS posts')
    cursor.execute('DROP TABLE IF EXISTS events')
    
    conn.commit()
    conn.close()
    
def fetch_all_events():
    """
    Fetches all events from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    
    return events

def fetch_event_by_type():
    """
    Fetches events from the database grouped by event type.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT event, COUNT(*) FROM events GROUP BY event')
    events = cursor.fetchall()
    conn.close()
    
    return events

def fetch_event_by_extension():
    """
    Fetches events from the database grouped by file extension.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT file_extension, COUNT(*) FROM events GROUP BY file_extension')
    events = cursor.fetchall()
    conn.close()
    
    return events

def fetch_event_by_after_date(theDate: str):
    """
    Fetches events from the database that occurred after a specified date.
    :param date: The date in 'YYYY-MM-DD' format.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE event_timestamp > ?', (theDate,))
    events = cursor.fetchall()
    conn.close()
    
    return events
    
def export_to_csv(theFilename: str):
    """
    Exports all events from the database to a CSV file.
    :param filename: The name of the CSV file to export to.
    """
    events = fetch_all_events()
    
    with open(theFilename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Filename', 'File Extension', 'Event Timestamp', 'File Size', 'Event'])
        writer.writerows(events)
    
    print(f"Data exported to {theFilename} successfully.")
    
def get_event_count():
    """
    Returns the total number of events in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM events')
    count = cursor.fetchone()[0]
    conn.close()
    
    return count

def get_event_by_id(theEventId: int):
    """
    Fetches a specific event by its ID.
    :param event_id: The ID of the event to fetch.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE id = ?', (theEventId,))
    event = cursor.fetchone()
    conn.close()
    
    return event