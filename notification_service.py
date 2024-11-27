from kafka import KafkaConsumer
import json

def notify_user(event):
    if "error" in event:
        print(f"ERROR: Certificate {event['id']} - {event['error']}")
    else:
        print(f"SUCCESS: Certificate {event['id']} verified for {event['name']}")

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "certificate.verified",
        "certificate.errors",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id="notification-service"
    )

    for message in consumer:
        notify_user(message.value)
