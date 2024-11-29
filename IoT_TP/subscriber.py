import paho.mqtt.client as mqtt
import time
import sys
import json

from processor import Processor
from repository import MovementDatabase

db = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")

processor = Processor(db)

def on_message(client, userdata, message):
    print("MESSAGE RECEIVED: ")
    try:
        payload = str(message.payload.decode("utf-8"))
        msgs = json.loads(payload)
        topic = message.topic
        print(f"Topic: {topic}")
        processor.process_message(topic, msgs)
    except Exception as e:
        print(f"Error processing or storing message: {e}")
    print("")


def main():
    broker = "127.0.0.1"
    dynamic_topic = "idc/64852"
    static_topic = "idc/64852/static"
    port = 1883

    timeout = 300

    client = mqtt.Client(client_id="subscriber")
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(dynamic_topic)
    client.subscribe(static_topic)
    start = time.time()
    elapsed = 0

    print("Subscribed, now waiting for messages ...")
    while elapsed != timeout:
        try:
            elapsed = int(time.time() - start)
            client.loop()
        except KeyboardInterrupt:
            client.loop_stop()
            sys.exit()

if __name__ == "__main__":
    main()