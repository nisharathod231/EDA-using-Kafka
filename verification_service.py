from kafka import KafkaConsumer, KafkaProducer
import json

def verify_certificate(cert):
    # Dummy verification logic
    if cert["certificate"].startswith("Cert"):
        return {"status": "verified", "id": cert["id"], "name": cert["name"]}
    else:
        return {"status": "error", "id": cert["id"], "error": "Invalid certificate"}

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "certificate.requests",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id="verification-service"
    )

    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for message in consumer:
        cert = message.value
        result = verify_certificate(cert)
        if result["status"] == "verified":
            producer.send("certificate.verified", value=result)
        else:
            producer.send("certificate.errors", value=result)
        print(f"Processed: {result}")
