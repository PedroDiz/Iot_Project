import paho.mqtt.client as mqtt
import sys
import json
from processor import Processor
from repository import MovementDatabase

broker = "127.0.0.1"
port = 1883

db = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")
processor = Processor(db)

def on_message(client, userdata, message):
    print("MESSAGE RECEIVED: ")
    try:
        payload = str(message.payload.decode("utf-8"))
        msgs = json.loads(payload)
        processor.process_message(message.topic, msgs)
    except Exception as e:
        print(f"Error processing or storing message: {e}")


def main():
    dynamic_topic = "idc/64852"
    static_topic = "idc/64852/static"

    client = mqtt.Client(client_id="subscriber")
    client.on_message = on_message
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