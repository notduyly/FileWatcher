import csv
import os
from datetime import datetime
import getpass
from .database import get_connection


def insert_event(theEvent, thePath):
    """
    Inserts a single event into the database.
    
    Args:
        theEvent: The type of event ('created', 'modified', 'deleted').
        thePath: The file path where the event occurred.
    """
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
    """
    Deletes a specific event from the database by its ID.
    
    Args:
        theEventId: The unique ID of the event to delete.
    """
    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            conn.execute('DELETE FROM events WHERE id = ?', (theEventId,))

def reset_database():
    """
    Resets the database.
    
    Returns:
        bool: True if reset was successful, False if an error occurred.
        
    Note:
        This operation is irreversible and will delete all stored events.
    """
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
    """
    Retrieves all events from the database.
    
    Returns:
        list: List of all event records, or empty list if error.
    """
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        return cursor.fetchall()

def fetch_event_by_type(theEventType='All'):
    """
    Retrieves events filtered by event type.
    
    Args:
        theEventType: The event type to filter by. Defaults to 'All' to retrieve all events.
    
    Returns:
        list: List of events matching the specified type.
    """
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
    """
    Retrieves events filtered by file extension.
    
    Args:
        theExtension: The file extension to filter by. Defaults to 'All' to retrieve all events.
    
    Returns:
        list: List of events with matching file extension.
    """
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
    """
    Retrieves events filtered by date range.
    
    Args:
        theDateRange: The date range filter. Options include:
            'All', 'Today', 'Last 7 days', 'Last 30 days'.
            Defaults to 'All'.
    
    Returns:
        list: List of events within the specified date range.
    """
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
    """
    Gets the total number of events in the database.
    
    Returns:
        int: Total count of events, or 0 if database connection fails.
    """
    with get_connection() as conn:
        if conn is None:
            return 0
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM events')
        return cursor.fetchone()[0]

def get_event_by_id(theEventId: int):
    """
    Retrieves a specific event by its unique ID.
    
    Args:
        theEventId: The unique ID of the event.
    
    Returns:
        tuple or None: Event data if found, None if not found or on error.
    """
    with get_connection() as conn:
        if conn is None:
            return None
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE id = ?', (theEventId,))
        return cursor.fetchone()

def query_events(theFilters=None):
    """
    Query events with multiple filter criteria.
    
    Args:
        theFilters: Dictionary containing filter criteria:
            - 'event_type': Filter by event type
            - 'extension': Filter by file extension  
            - 'date_range': Filter by date range
            Defaults to None (no filters applied).
    
    Returns:
        list: List of events matching all specified filters,
    """
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
    """
    Gets all unique file extensions from the events table.
    
    Returns:
        list: List of unique file extensions found in the database,
    """
    with get_connection() as conn:
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT file_extension FROM events WHERE file_extension != ""')
        extensions = cursor.fetchall()
        return ['All'] + [ext[0] for ext in extensions if ext[0]]

def save_multiple_events(theEvents):
    """
    Save multiple events to the database in a single transaction.
    
    Args:
        theEvents: List of event dictionaries, each containing:
            - 'filepath': Path to the file
            - 'event_type': Type of file system event
    
    Returns:
        bool: True if all events were saved successfully, False otherwise.
    """
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
    """
    Format a database event record for display.
    
    Args:
        theEvent: Raw event data from database query.
        
    Returns:
        tuple: Formatted event data containing:
            - filename: Base filename without path
            - extension: File extension or "(none)" if empty
            - display_path: Relative path for display
            - event_type: Type of file system event
            - timestamp: When the event occurred
    """
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
    """
    Exports event data to a CSV file.
    
    Args:
        thePath: Full path where the CSV file should be saved.
        theEvents: List of events to export.
    
    Returns:
        bool: True if export was successful, False if an error occurred.
    """
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