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
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')