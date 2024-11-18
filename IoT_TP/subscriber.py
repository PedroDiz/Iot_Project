import paho.mqtt.client as mqtt
import time
import sys
import json

def on_message(client, userdata, message):
    print("MESSAGE RECEIVED: ")
    payload = str(message.payload.decode("utf-8"))
    msgs = json.loads(payload)
    print(msgs)
    print("")


def main():
    broker = "192.168.100.2"
    topic = "idc/fc64852"
    port = 1883

    timeout = 300

    client = mqtt.Client(client_id="subscriber")
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(topic)
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