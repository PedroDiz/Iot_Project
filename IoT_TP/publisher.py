import sys
import json
import time
from datetime import datetime

import paho.mqtt.client as mqtt

broker = "127.0.0.1"
port = 1883

def load_file_data(filepath):
    dataset = []
    try:
        with open(filepath, 'r') as file:
            header = file.readline().strip().split(";")
            for line in file:
                values = line.strip().split(";")
                record = {key: float(value) for key, value in zip(header, values)}
                dataset.append(record)

    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return dataset

def send_static_data(mqttc, static_data, static_topic):
    try:
        static_payload = json.dumps(static_data)
        print("Sending static data: " + static_payload)
        mqttc.publish(static_topic, static_payload)
    except Exception as e:
        print(f"Error sending static data: {e}")
        sys.exit(1)

def send_dynamic_data(mqttc, dataset, dynamic_topic, num_msgs_send, delay):
    for i in range(num_msgs_send):
        try:
            data_to_send = append_time_to_data(dataset[i])
            payload = json.dumps(data_to_send)
            print("Sending dynamic msg: " + payload)
            mqttc.publish(dynamic_topic, payload)
            time.sleep(delay)
        except KeyboardInterrupt:
            sys.exit()
        finally:
            mqttc.loop_stop()

def append_time_to_data(data):
    currentDateTime = datetime.now()
    data["date"] = currentDateTime.strftime("%d/%m/%Y")
    data["time"] = currentDateTime.strftime("%H:%M:%S")
    return data


def main():
    dynamic_topic = "idc/64852"
    static_topic = "idc/64852/static"
    delay = 1
    filepath = "data.txt"

    static_data = {
        "bodyweight": 70,
        "height": 1.75,
        "age": 30,
        "gender" : "male"
    }

    # Load dynamic sensor data
    dataset = load_file_data(filepath)
    num_msgs_send = len(dataset)

    # Initialize MQTT client
    mqttc = mqtt.Client("Publisher")
    mqttc.connect(broker, port)
    mqttc.loop_start()

    # Publish static user data
    send_static_data(mqttc, static_data, static_topic)

    # Publish dynamic sensor data
    send_dynamic_data(mqttc, dataset, dynamic_topic, num_msgs_send, delay)


if __name__ == "__main__":
    main()