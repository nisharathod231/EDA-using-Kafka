import json
import sqlite3
from confluent_kafka import Consumer

# Kafka Consumer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'notifier-consumer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

# SQLite database setup
conn = sqlite3.connect('documents.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS documents
                  (name TEXT, document_id TEXT, status TEXT)''')

# Subscribe to 'verification_completed' topic
consumer.subscribe(['verification_completed'])

def display_status(message):
    # Display the status message
    name = message['name']
    document_id = message['document_id']
    status = message['status']
    print(f"{name}'s {document_id} is {status}")
    
    # Store in the SQLite database
    cursor.execute("INSERT INTO documents (name, document_id, status) VALUES (?, ?, ?)",
                   (name, document_id, status))
    conn.commit()

def consume_verification_status():
    print("Notifier is listening...")

    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue
        
        message = json.loads(msg.value().decode('utf-8'))
        print(f"Consumed Status: {message}")
        
        # Display and store the status
        display_status(message)

if __name__ == "__main__":
    consume_verification_status()
