from kafka import KafkaProducer, KafkaConsumer
import json

def create_producer():
    return KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        group_id='certificate-verification-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
