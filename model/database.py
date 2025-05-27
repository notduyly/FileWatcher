import sqlite3

def get_connection():
    try:
        return sqlite3.connect('database.db')
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

def init_db():
    with get_connection() as conn:
        if conn is None:
            return
        with conn:
            # Create file_events table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS file_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_directory BOOLEAN DEFAULT 0
                )
            ''')

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")