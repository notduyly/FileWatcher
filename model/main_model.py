from database import init_db, insert_event, get_connection, fetch_all_events, delete_event, reset_db

if __name__ == "__main__":
    # init_db()
    
    insert_event("test.txt", "adding event", 1234)
    
    # reset_db()
    
    # delete_event(1)
    
    events = fetch_all_events()

    for event in events:
        print(event)
    print("Database initialized and event inserted successfully.")
