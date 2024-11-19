import sys
import json
import time
from datetime import datetime

import paho.mqtt.client as mqtt
import signal


def signal_handler(sig, frame):
    print('You pressed Ctrl+C.\nProgram closed.')
    sys.exit(0)

def load_file_data(filepath):
    dataset = []
    try:
        with open(filepath, 'r') as file:
            # Get header values
            header = file.readline().strip().split(";")

            # Process each subsequent line in the file
            for line in file:
                values = line.strip().split(";")
                record = {key: float(value) for key, value in zip(header, values)}

                currentDateTime = datetime.now()
                record["date"] = currentDateTime.strftime("%d/%m/%Y")
                record["time"] = currentDateTime.strftime("%H:%M:%S")
                dataset.append(record)

    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return dataset


def main(argv):
    signal.signal(signal.SIGINT, signal_handler)

    broker = "127.0.0.1"
    port = 1883
    topic = "idc/fc64852"
    delay = 1
    filepath = "data.txt"
    dataset = load_file_data(filepath)
    num_msgs_send = len(dataset)

    mqttc = mqtt.Client("Publisher")
    mqttc.connect(broker, port)
    msgs_sent = 0
    mqttc.loop_start()

    for i in range(num_msgs_send):
        try:
            payload = json.dumps(dataset[i])
            print("Sending msg: " + payload)
            mqttc.publish(topic, payload)
            msgs_sent += 1
            time.sleep(delay)
        except KeyboardInterrupt:
            sys.exit()
    mqttc.loop_stop()

    print("Messages sent: " + str(msgs_sent))


if __name__ == "__main__":
    main(sys.argv[1:])