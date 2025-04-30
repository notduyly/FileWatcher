import _sqlite3

def get_connection():
    """
    Returns a connection to the SQLite database.
    """
    try:
        conn = _sqlite3.connect('database.db')
        return conn
    except _sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None
    
def init_db():
    """
    Initializes the database by creating the necessary tables.
    """
    conn = get_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # Create posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
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

def insert_event(theFilename, theEvent):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO events (filename, event)
        VALUES (?, ?)
    ''', (theFilename, theEvent))
    conn.commit()
    conn.close()
    
def delete_event(event_id):
    """
    Deletes an event from the database by its ID.
    """
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM events WHERE id = ?
    ''', (event_id,))
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