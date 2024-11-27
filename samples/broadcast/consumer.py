from kafka import KafkaConsumer
import json
import sys
from utils import TOPIC


def consume_messages(consumer_id):
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=["kafka:29092"],
        group_id=f"chat-group-{consumer_id}",
        # Earliest: Read from the oldest message
        # Latest: Read from the latest message
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        api_version=(7, 5, 0),
    )

    print(f"Consumer {consumer_id} started listening...Topic: {TOPIC}")

    for message in consumer:
        print(f"\nConsumer {consumer_id} received: {message.value}")
        print("> ", end="", flush=True)


if __name__ == "__main__":
    consumer_id = sys.argv[1]
    consume_messages(consumer_id)
