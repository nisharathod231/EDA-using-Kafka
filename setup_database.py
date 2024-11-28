import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('event_state.db')
cursor = conn.cursor()

# Create a table to store document statuses
cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    type TEXT,
    name TEXT,
    status TEXT
)''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup completed. 'event_state.db' created.")
