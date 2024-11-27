from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import sys
from datetime import datetime
from utils import TOPIC


def setup_producer():
    return KafkaProducer(
        bootstrap_servers=["kafka:29092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
        api_version=(7, 5, 0),
    )


def setup_consumer(username):
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=["kafka:29092"],
        group_id=f"chat-group-{username}",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        api_version=(7, 5, 0),
    )


def receive_messages(consumer, username):
    for message in consumer:
        data = message.value
        # Don't print our own messages
        if data["username"] != username:
            print(f"\n{data['username']}: {data['message']}")
            print(f"{username}> ", end="", flush=True)


def send_messages(producer, username):
    try:
        while True:
            message = input(f"{username}> ")
            data = {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "username": username,
            }
            producer.send(TOPIC, value=data, key=username)
            producer.flush()
    except KeyboardInterrupt:
        producer.close()
        print("\nExiting chat...")
        sys.exit(0)


def start_chat():
    if len(sys.argv) > 3:
        print("Usage: python chat_client.py <username> [earliest|latest]")
        sys.exit(1)

    username = sys.argv[1]
    producer = setup_producer()
    consumer = setup_consumer(username)

    print(f"Welcome to the chat room, {username}!")
    print("Type your messages (press Ctrl+C to exit)")

    # Start consumer thread
    consumer_thread = threading.Thread(
        target=receive_messages, args=(consumer, username), daemon=True
    )
    consumer_thread.start()

    # Start producer in main thread
    send_messages(producer, username)


if __name__ == "__main__":
    start_chat()
