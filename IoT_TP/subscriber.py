import paho.mqtt.client as mqtt
import time
import sys
import json
from repository import MovementDatabase

db = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")
topic_id = "64852"

def on_message(client, userdata, message):
    print("MESSAGE RECEIVED: ")
    try:
        payload = str(message.payload.decode("utf-8"))
        msgs = json.loads(payload)
        print(msgs)

        db.insert_movement(
            id=topic_id,
            acceleration_x=msgs["acceleration_x"],
            acceleration_y=msgs["acceleration_y"],
            acceleration_z=msgs["acceleration_z"],
            gyro_x=msgs["gyro_x"],
            gyro_y=msgs["gyro_y"],
            gyro_z=msgs["gyro_z"],
            movement_data=msgs["movement_data"],
            movement_time=msgs["movement_time"]
        )

    except Exception as e:
        print(f"Error processing or storing message: {e}")
    print("")


def main():
    broker = "127.0.0.1"
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