import kafka_utils

def send_certificate_request(certificate):
    producer = kafka_utils.create_producer()
    producer.send('certificate-verification-requests', certificate)
    producer.flush()
    print("Certificate request sent:", certificate)

if __name__ == "__main__":
    certificate_data = {
        "id": "12345",
        "name": "John Doe",
        "issued_by": "XYZ University",
        "valid_until": "2025-12-31"
    }
    send_certificate_request(certificate_data)
