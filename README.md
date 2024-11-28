# Project Report: Demonstrating Mediator Topology in Event-Driven Architecture with Kafka

## Introduction
In this project, we demonstrate an Event-Driven Architecture (EDA) with a focus on the Mediator Topology, implemented using Apache Kafka. The system revolves around document verification, where documents are processed based on whether they belong to Education or Employment categories. The architecture consists of multiple components, with each responsible for a specific task in the document verification process. This system processes documents using Kafka topics and directs data between processors (mediator) based on the document type (education or employment).

---

## Implementation Details

The system simulates document verification using Kafka for event-based communication. Below is a detailed explanation of how each component works and how the system was implemented.

<img width="474" alt="Screenshot 2024-11-28 at 4 09 26 PM" src="https://github.com/user-attachments/assets/36bf6c40-2b24-495a-8cf3-2c25b8f80714">


### 1. Kafka Topics Setup
To get started with Kafka, the following steps were followed:

1. Extract the contents of the tar archive:
    ```bash
    tar -xvf kafka_2.13-3.8.0.tar
    ```
2. Change into the Kafka directory:
    ```bash
    cd kafka_2.13-3.8.0
    ```
3. Start the Zookeeper service:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    ```
4. Start the Kafka broker:
    ```bash
    bin/kafka-server-start.sh config/server.properties
    ```
5. Create the necessary Kafka topics:
    ```bash
    kafka-topics.sh --create --topic event_queue --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    kafka-topics.sh --create --topic educational_documents --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    kafka-topics.sh --create --topic employment_documents --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    kafka-topics.sh --create --topic verification_completed --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
6. Verify the topics were created:
    ```bash
    bin/kafka-topics.sh --list --bootstrap-server localhost:9092
    ```

### 2. Document Verification Logic in Python
The main logic is implemented in Python using the kafka-python library to produce and consume events. The flow of the system is as follows:

#### Main Producer (main.py):
- The main producer accepts inputs for name and document_id from the user.
- Based on the document_id, it determines whether the document is for education or employment.
- The producer sends the document details to the `event_queue` Kafka topic.

#### Mediator (mediator.py):
- The mediator listens to the `event_queue` for new events.
- It checks the document type based on the document_id. If it is numeric, it directs the event to the `educational_documents` topic. If it is alphanumeric, it directs the event to the `employment_documents` topic.

#### Processors:
- **Educational Processor (educational_processor.py)**: This processor checks if the document_id is 4 digits long. If valid, it updates the status to "Valid"; otherwise, it sets it to "Invalid".
- **Employment Processor (employment_processor.py)**: Similar to the educational processor, this processor checks if the document_id is 4 digits long for employment documents.

#### Consumer Notification (consumer_notification.py):
- Once the processor completes the verification, it sends the result (valid or invalid) to the `verification_completed` topic.
- The consumer listens to this topic and displays a message to the user, such as: "Name's document_id is Valid/Invalid".

#### SQLite Database:
- The status of each document is saved in an SQLite database, including the name, document_id, and status.
- This is achieved using the sqlite3 library in Python.

## Outputs:

<img width="1440" alt="Screenshot 2024-11-28 at 4 10 58 PM" src="https://github.com/user-attachments/assets/fa5437de-ffd3-4712-a9ed-7cd60a8cbc1e">
