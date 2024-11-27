from kafka import KafkaProducer
import json
from datetime import datetime
from utils import TOPIC
import uuid


def produce_messages():
    # Key will be used to determine which partition the message will be sent to
    key = str(uuid.uuid4())
    producer = KafkaProducer(
        bootstrap_servers=["kafka:29092"],
        # Serialize the value to JSON and then to bytes
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
        api_version=(7, 5, 0),
    )

    print("Producer started. Type messages to publish (press Ctrl+C to exit):")
    try:
        while True:
            message = input("> ")
            data = {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "producer_id": "BROADCAST_PRODUCER",
            }
            # Randomize the key to ensure that the message is sent to a different partition
            # key = str(uuid.uuid4())
            producer.send(TOPIC, value=data, key=key)
            producer.flush()  # Ensure the message is sent immediately
            print(f"Published: {data} to Topic: {TOPIC}")

    except KeyboardInterrupt:
        producer.close()
        print("\nProducer stopped.")


if __name__ == "__main__":
    produce_messages()
