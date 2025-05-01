import _sqlite3
import csv
from database import get_connection

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

def fetch_event_by_after_date(date: str):
    """
    Fetches events from the database that occurred after a specified date.
    :param date: The date in 'YYYY-MM-DD' format.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE event_timestamp > ?', (date,))
    events = cursor.fetchall()
    conn.close()
    
    return events

def insert_event(theFilename: str, theEvent: str, theFileSize: int):
    """
    Insert a file event with additional metadata
    """
    conn = get_connection()
    if conn is None:
        return
    
    # Split filename to get extension
    file_extension = theFilename.split('.')[-1] if '.' in theFilename else ''
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (filename, file_extension, file_size, event)
        VALUES (?, ?, ?, ?)
    ''', (theFilename, file_extension, theFileSize, theEvent))
    
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
    
def export_to_csv(filename: str):
    """
    Exports all events from the database to a CSV file.
    :param filename: The name of the CSV file to export to.
    """
    events = fetch_all_events()
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Filename', 'File Extension', 'Event Timestamp', 'File Size', 'Event'])
        writer.writerows(events)
    
    print(f"Data exported to {filename} successfully.")
    
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

def get_event_by_id(event_id: int):
    """
    Fetches a specific event by its ID.
    :param event_id: The ID of the event to fetch.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()
    conn.close()
    
    return event