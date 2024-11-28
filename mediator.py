import json
from confluent_kafka import Consumer, Producer

# Kafka Consumer and Producer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mediator-consumer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Subscribe to the 'event_queue' topic
consumer.subscribe(['event_queue'])

def route_event(message):
    # Route event to the correct processor topic
    document_type = message['document_type']
    
    if document_type == "education":
        producer.produce('educational_documents', value=json.dumps(message))
    else:
        producer.produce('employment_documents', value=json.dumps(message))
    
    producer.flush()

def consume_events():
    print("Mediator is listening for events...")

    while True:
        # Consume messages from 'event_queue'
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue
        
        message = json.loads(msg.value().decode('utf-8'))
        print(f"Consumed: {message}")
        
        # Route the event to the appropriate processor
        route_event(message)

if __name__ == "__main__":
    consume_events()
