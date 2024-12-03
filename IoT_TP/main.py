import json

import paho.mqtt.client as mqtt
from processor.processors import ActivityTimeProcessor, CaloriesProcessor, StepProcessor
from processor.repository import MovementDatabase

repo = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")

def main():
    movements = repo.retrieve_movement(64852)

    for movement in movements:
        print(movement)

    activity_processor = ActivityTimeProcessor()
    activity_time = activity_processor.process(movements)
    print("Activity Time: ")
    print(activity_time)

    broker = "127.0.0.1"
    port = 1883
    topic = "activity_time"
    client = mqtt.Client(client_id="publisher")
    client.connect(broker, port)
    client.loop_start()

    data_to_send = {
        "activity_time": activity_time,
    }

    # Print the data to be sent
    print("Data to be sent: ")
    print(data_to_send)

    try:
        payload = json.dumps(data_to_send)
        print("Sending dynamic msg: " + payload)
        client.publish(topic, payload)
    except KeyboardInterrupt:
        print("Error sending data")
    finally:
        client.loop_stop()



if __name__ == "__main__":
    main()