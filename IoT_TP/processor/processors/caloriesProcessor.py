import json

import paho.mqtt.client as mqtt


class CaloriesProcessor:

    velocity_map = {
        range(20, 30): {"male": 1.36, "female": 1.34},
        range(30, 40): {"male": 1.43, "female": 1.34},
        range(40, 50): {"male": 1.45, "female": 1.39},
        range(50, 60): {"male": 1.43, "female": 1.31},
        range(60, 70): {"male": 1.34, "female": 1.24},
        range(70, 80): {"male": 1.26, "female": 1.13},
        range(80, 90): {"male": 0.97, "female": 0.94},
    }

    def process(self, person_data, movement_data):

        # Retrieve age, weight, height, gender from person_data
        age = person_data[1]
        gender = person_data[2]
        weight = person_data[3]
        height = person_data[4]

        # Retrieve activity from movement_data
        activity_values = [item[2] for item in movement_data]

        # Calculate burnt calories
        for age_range, genders in self.velocity_map.items():
            if age in age_range:
                velocity = genders.get(gender)
                break

        # Split the activity array into blocks of 60 and apply the formula
        # Depending on the activity, the velocity is multiplied by 2
        # An average is taken of the activity values in the block

        burnt_calories = 0
        for i in range(0, len(activity_values), 60):
            chunk = activity_values[i:i+60]
            activity = sum(chunk) / len(chunk)
            # If the activity average is above 0.5 multiply the velocity by 2
            temp_velocity = velocity

            if activity > 0.5:
                temp_velocity *= 2

            burnt_calories += ((0.035 * weight + ((temp_velocity ** 2) / height) * 0.029 * weight) / 60) * len(chunk)
        return round(burnt_calories)

    def send_data_to_nodered(self, burnt_calories):

        broker = "172.100.10.10"
        port = 1883
        topic = "calories"
        client = mqtt.Client(client_id="publisher")
        client.connect(broker, port)
        client.loop_start()

        data_to_send = {
            "calories_burned": burnt_calories,
        }

        try:
            payload = json.dumps(data_to_send)
            print("Sending dynamic msg: " + payload)
            client.publish(topic, payload)
        except KeyboardInterrupt:
            print("Error sending data")
        finally:
            client.loop_stop()

