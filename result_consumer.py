import kafka_utils

def consume_results():
    consumer = kafka_utils.create_consumer('certificate-verification-results')
    for message in consumer:
        result = message.value
        print("Received verification result:", result)

if __name__ == "__main__":
    consume_results()
