import json
from confluent_kafka import Producer
import sqlite3

# Kafka Producer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'document-producer'
}

producer = Producer(conf)

def produce_event(name, document_id):
    # Determine document type based on the ID
    document_type = "education" if document_id.isnumeric() else "employment"
    
    # Create the event message
    event_message = {
        'name': name,
        'document_id': document_id,
        'document_type': document_type
    }
    
    # Send the event to Kafka 'event_queue'
    producer.produce('event_queue', value=json.dumps(event_message))
    producer.flush()

    print(f"Produced: {event_message}")

def main():
    # User input for name and document_id
    name = input("Enter the name: ")
    document_id = input("Enter the document_id: ")
    
    # Produce the event
    produce_event(name, document_id)

if __name__ == "__main__":
    main()
