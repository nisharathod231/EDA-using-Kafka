from kafka import KafkaProducer
import json
import time

def send_certificate_requests(producer, topic):
    certificates = [
        {"id": 1, "name": "John Doe", "certificate": "Cert123"},
        {"id": 2, "name": "Jane Smith", "certificate": "Bert456"},
        {"id": 3, "name": "Alice Brown", "certificate": "Cert789"}
    ]
    for cert in certificates:
        producer.send(topic, value=cert)
        print(f"Sent: {cert}")
        time.sleep(1)

if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    send_certificate_requests(producer, "certificate.requests")
