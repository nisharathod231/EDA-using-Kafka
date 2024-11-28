import json
from confluent_kafka import Consumer, Producer

# Kafka Consumer and Producer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'employment-processor',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Subscribe to 'employment_documents' topic
consumer.subscribe(['employment_documents'])

def validate_employment_document(message):
    document_id = message['document_id']
    
    # Check if document ID is 4 characters long
    if len(document_id) == 4 and document_id.isalpha():
        status = "Valid"
    else:
        status = "Invalid"
    
    # Update the message with validation status
    message['status'] = status
    producer.produce('verification_completed', value=json.dumps(message))
    producer.flush()
    print(f"Processed Employment Document: {message}")

def consume_employment_documents():
    print("Employment Processor is listening...")

    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue
        
        message = json.loads(msg.value().decode('utf-8'))
        print(f"Consumed Employment Document: {message}")
        
        # Validate the employment document
        validate_employment_document(message)

if __name__ == "__main__":
    consume_employment_documents()
