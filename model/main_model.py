from database import init_db, insert_event, get_connection, fetch_all_events, delete_event, reset_db

if __name__ == "__main__" and get_connection() is None:
    init_db()
    # reset_db()
    
    events = fetch_all_events()

    for event in events:
        print(event)
    print("Database initialized and event inserted successfully.")
