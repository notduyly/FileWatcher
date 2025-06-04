import sqlite3

def get_connection():
    try:
        return sqlite3.connect('database.db')
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

def _init_db():
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
    print("Initializing database...")
    _init_db()
    print("Database initialized successfully!")