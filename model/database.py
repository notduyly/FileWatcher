import sqlite3

def get_connection():
    """
    Establish and return a connection to the SQLite database.
    
    Returns:
        Database connection object if successful, None if connection failed.
        
    Raises:
        sqlite3.Error: If there's an error connecting to the database.
    """
    try:
        return sqlite3.connect('database.db')
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

def _init_db():
    """
    Initialize the database.
    
    Creates the 'events' table with the following schema:
    - id: Primary key (auto-increment)
    - filename: Name of the file (TEXT, NOT NULL)
    - file_path: Full path to the file (TEXT, NOT NULL) 
    - file_extension: File extension (TEXT, NOT NULL)
    - event: Type of file system event (TEXT, NOT NULL)
    - event_timestamp: When the event occurred (DATETIME, defaults to current time)
    - file_size: Size of the file in bytes (INTEGER)
    - user: User who triggered the event (TEXT)
    
    """
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
                    user TEXT
                )
            ''')

if __name__ == "__main__":
    """
    Script for standalone database initialization.
    """
    print("Initializing database...")
    _init_db()
    print("Database initialized successfully!")