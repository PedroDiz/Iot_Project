import functools

import paho.mqtt.client as mqtt
import sys
import json
from processor import Processor
from repository import MovementDatabase

def on_message(client, userdata, message, processor):
    print("MESSAGE RECEIVED: ")
    try:
        payload = str(message.payload.decode("utf-8"))
        msgs = json.loads(payload)
        processor.process_message(message.topic, msgs)
    except Exception as e:
        print(f"Error processing or storing message: {e}")


def main():

    broker = "172.100.10.10"
    port = 1883

    db = MovementDatabase("172.100.10.20", "db", "dbuser", "changeit")
    processor = Processor(db)

    dynamic_topic = "idc/64852"
    static_topic = "idc/64852/static"

    client = mqtt.Client(client_id="subscriber")
    client.on_message = functools.partial(on_message, processor=processor)
    client.connect(broker, port)
    client.subscribe(dynamic_topic)
    client.subscribe(static_topic)

    print("Subscribed, now waiting for messages ...")
    while True:
        try:
            client.loop()
        except KeyboardInterrupt:
            client.loop_stop()
            sys.exit()

if __name__ == "__main__":
    main()