import json
from confluent_kafka import Consumer, Producer

# Kafka Consumer and Producer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'educational-processor',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Subscribe to 'educational_documents' topic
consumer.subscribe(['educational_documents'])

def validate_educational_document(message):
    document_id = message['document_id']
    
    # Check if document ID is 4 digits long
    if len(document_id) == 4 and document_id.isdigit():
        status = "Valid"
    else:
        status = "Invalid"
    
    # Update the message with validation status
    message['status'] = status
    producer.produce('verification_completed', value=json.dumps(message))
    producer.flush()
    print(f"Processed Educational Document: {message}")

def consume_educational_documents():
    print("Educational Processor is listening...")

    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue
        
        message = json.loads(msg.value().decode('utf-8'))
        print(f"Consumed Educational Document: {message}")
        
        # Validate the educational document
        validate_educational_document(message)

if __name__ == "__main__":
    consume_educational_documents()
