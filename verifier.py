import kafka_utils

def verify_certificate(certificate):
    # Simulate certificate verification logic
    is_valid = certificate["valid_until"] > "2024-11-26"  # Replace with actual date comparison logic
    return {
        "id": certificate["id"],
        "status": "valid" if is_valid else "invalid",
        "details": certificate
    }

def process_requests():
    consumer = kafka_utils.create_consumer('certificate-verification-requests')
    producer = kafka_utils.create_producer()

    for message in consumer:
        certificate = message.value
        print("Processing certificate:", certificate)
        result = verify_certificate(certificate)
        producer.send('certificate-verification-results', result)
        producer.flush()
        print("Verification result sent:", result)

if __name__ == "__main__":
    process_requests()
