import sqlite3
import csv
import os
from datetime import datetime
import getpass
from .database import get_connection


def insert_event(theEvent, thePath):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    abs_path = os.path.abspath(thePath)
    file_name = os.path.basename(abs_path)
    file_extension = os.path.splitext(file_name)[1]
    file_size = os.path.getsize(abs_path) if os.path.isfile(abs_path) else None
    user = getpass.getuser()

    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            conn.execute("""
                INSERT INTO events (
                    filename, file_path, file_extension, event,
                    event_timestamp, file_size, user
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                file_name, abs_path, file_extension, theEvent,
                timestamp, file_size, user
            ))

def delete_event(theEventId: int):
    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            conn.execute('DELETE FROM events WHERE id = ?', (theEventId,))

def reset_database():
    with get_connection() as conn:
        if conn is None:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS events')
            from .database import _init_db
            _init_db()
            return True
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False

def fetch_all_events():
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        return cursor.fetchall()

def fetch_event_by_type(theEventType='All'):
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        
        if theEventType == 'All':
            cursor.execute('''
                SELECT * FROM events 
                ORDER BY event_timestamp DESC
            ''')
        else:
            cursor.execute('''
                SELECT * FROM events 
                WHERE event = ? 
                ORDER BY event_timestamp DESC
            ''', (theEventType,))
            
        return cursor.fetchall()

def fetch_event_by_extension(theExtension='All'):
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        
        if theExtension == 'All':
            cursor.execute('''
                SELECT * FROM events 
                ORDER BY event_timestamp DESC
            ''')
        else:
            cursor.execute('''
                SELECT * FROM events 
                WHERE file_extension = ? 
                ORDER BY event_timestamp DESC
            ''', (theExtension,))
            
        return cursor.fetchall()

def fetch_event_by_after_date(theDateRange='All'):
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        
        if theDateRange == 'All':
            cursor.execute('SELECT * FROM events ORDER BY event_timestamp DESC')
        elif theDateRange == 'Today':
            cursor.execute('SELECT * FROM events WHERE DATE(event_timestamp) = DATE("now") ORDER BY event_timestamp DESC')
        elif theDateRange == 'Last 7 days':
            cursor.execute('SELECT * FROM events WHERE event_timestamp >= datetime("now", "-7 days") ORDER BY event_timestamp DESC')
        elif theDateRange == 'Last 30 days':
            cursor.execute('SELECT * FROM events WHERE event_timestamp >= datetime("now", "-30 days") ORDER BY event_timestamp DESC')
        
        return cursor.fetchall()

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

def query_events(theFilters=None):
    with get_connection() as conn:
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM events WHERE 1=1"
            params = []
            
            if theFilters:
                if theFilters.get('event_type') and theFilters['event_type'] != 'All':
                    query += " AND event LIKE ?"
                    params.append(f"%{theFilters['event_type']}%")
                
                if theFilters.get('extension') and theFilters['extension'] != 'All':
                    query += " AND file_extension = ?"
                    params.append(theFilters['extension'])
                
                if theFilters.get('date_range') and theFilters['date_range'] != 'All':
                    if theFilters['date_range'] == 'Today':
                        query += " AND DATE(event_timestamp) = DATE('now')"
                    elif theFilters['date_range'] == 'Last 7 days':
                        query += " AND event_timestamp >= datetime('now', '-7 days')"
                    elif theFilters['date_range'] == 'Last 30 days':
                        query += " AND event_timestamp >= datetime('now', '-30 days')"
            
            query += " ORDER BY event_timestamp DESC"
            print(f"DEBUG - Query: {query}")
            print(f"DEBUG - Params: {params}")
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            print(f"DEBUG - Found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"Database error: {e}")
            return []

def get_unique_extensions():
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT file_extension FROM events WHERE file_extension != ""')
        extensions = cursor.fetchall()
        return ['All'] + [ext[0] for ext in extensions if ext[0]]

def save_multiple_events(theEvents):
    if not theEvents:
        return False
        
    try:
        with get_connection() as conn:
            if conn is None:
                return False
            
            cursor = conn.cursor()
            for event in theEvents:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file_path = event['filepath']
                filename = os.path.basename(file_path)
                extension = os.path.splitext(filename)[1]
                file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else None
                user = getpass.getuser()

                cursor.execute("""
                    INSERT INTO events (
                        filename, file_path, file_extension, event,
                        event_timestamp, file_size, user
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    filename, file_path, extension, event['event_type'],
                    timestamp, file_size, user
                ))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error saving events to database: {e}")
        return False

def format_event_for_display(theEvent):
    file_path = theEvent[2]
    filename = os.path.basename(file_path)
    extension = os.path.splitext(filename)[1] or "(none)"
    display_path = os.path.relpath(file_path)
    
    return (
        filename,
        extension,
        display_path,
        theEvent[4],
        theEvent[5]
    )

def export_events_to_csv(thePath, theEvents):
    try:
        with open(thePath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'Extension', 'Path', 'Event', 'Timestamp'])
            
            for event in theEvents:
                formatted_event = format_event_for_display(event)
                writer.writerow(formatted_event)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False