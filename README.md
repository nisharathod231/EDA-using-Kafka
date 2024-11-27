# Certificate Verification Event-Driven System Using Kafka

This project implements an event-driven architecture for certificate verification using Apache Kafka. The system enables scalable, loosely coupled microservices communication for processing certificate verification requests.

## Architecture

### Key Components

1. **Producer**
   - Sends certificate verification requests to Kafka topics
   - Simulates multiple event sources

2. **Kafka Topics**
   - Communication medium between services
   - Topics:
     - `certificate.requests`: New certificate verification requests
     - `certificate.verified`: Successful verification events
     - `certificate.errors`: Failed verification attempts or errors

3. **Consumers**
   - **Verification Service Consumer**: 
     - Listens to `certificate.requests`
     - Processes verification data
     - Sends results to `certificate.verified` or `certificate.errors`
   
   - **Notification Service Consumer**:
     - Listens to `certificate.verified` and `certificate.errors`
     - Sends alerts to users based on verification results

## Prerequisites

- Python 3.8+
- Apache Kafka
- ZooKeeper
- kafka-python library

## Project Structure

```bash
certificate-verification/
├── producer.py
├── verification_service.py      
├── notification_service.py   
├── kafka_utils.py       
```

## Setup and Installation

### 1. Install Dependencies

```bash
pip install kafka-python-ng
```

### 2. Start Kafka and ZooKeeper

```bash
cd kafka_2.13-3.8.0

# Start ZooKeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Broker
bin/kafka-server-start.sh config/server.properties
```

### 3. Create Kafka Topics

```bash
bin/kafka-topics.sh --create --topic certificate.requests --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic certificate.verified --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic certificate.errors --bootstrap-server localhost:9092
```

## Running the System

### Start Services in Separate Terminals

1. **Start Producer**
   ```bash
   python producer.py
   ```
   - Sends certificate verification requests to Kafka

2. **Start Verification Service**
   ```bash
   python verification_service.py
   ```
   - Processes certificate requests
   - Sends results to appropriate topics

3. **Start Notification Service**
   ```bash
   python notification_service.py
   ```
   - Listens for verification results
   - Notifies users

## Configuration

Modify `kafka_utils.py` to adjust:
- Kafka broker connection details
- Topic names
- Consumer group configurations
