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
    
    conn.commit()
    conn.close()