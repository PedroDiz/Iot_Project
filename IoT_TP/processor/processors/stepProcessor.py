import json

import paho.mqtt.client as mqtt


class StepProcessor:

    step_map = {
        (1.52, 1.54): {'female': 0.630, 'male': 0.633},
        (1.55, 1.56): {'female': 0.641, 'male': 0.643},
        (1.57, 1.59): {'female': 0.651, 'male': 0.653},
        (1.60, 1.62): {'female': 0.660, 'male': 0.663},
        (1.63, 1.64): {'female': 0.672, 'male': 0.676},
        (1.65, 1.67): {'female': 0.681, 'male': 0.686},
        (1.68, 1.69): {'female': 0.693, 'male': 0.698},
        (1.70, 1.72): {'female': 0.705, 'male': 0.711},
        (1.73, 1.74): {'female': 0.716, 'male': 0.721},
        (1.75, 1.77): {'female': 0.723, 'male': 0.724},
        (1.78, 1.79): {'female': 0.734, 'male': 0.737},
        (1.80, 1.82): {'female': 0.744, 'male': 0.748},
        (1.83, 1.84): {'female': 0.755, 'male': 0.757},
        (1.85, 1.87): {'female': 0.762, 'male': 0.764},
        (1.88, 1.90): {'female': 0.777, 'male': 0.779},
        (1.91, 1.92): {'female': 0.787, 'male': 0.790},
        (1.93, 1.95): {'female': 0.799, 'male': 0.803},
        (1.96, 1.98): {'female': 0.807, 'male': 0.813}
    }

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

        # Retrieve height, gender from person_data
        age = person_data[1]
        gender = person_data[2]
        height = person_data[4]

        # get the step length of the person
        step_length = 0

        for height_range, genders in self.step_map.items():
            if height_range[0] <= height < height_range[1]:  # Check if height is within the range
                step_length = genders.get(gender)
                break

        print(f"Step length: {step_length}")

        # get the velocity of the person
        velocity = 0

        for age_range, genders in self.velocity_map.items():
            if age in age_range:
                velocity = genders.get(gender)
                break

        print(f"Velocity: {velocity}")
        # get the different activity values
        activity_values = [item[2] for item in movement_data]

        nr_steps = 0
        for i in range(0, len(activity_values), 60):
            chunk = activity_values[i:i+60]
            activity = sum(chunk) / len(chunk)

            temp_velocity = velocity

            # If the activity average is above 0.5, temporarily multiply the velocity by 2 for this iteration
            if activity > 0.5:
                temp_velocity *= 2

            nr_steps += (temp_velocity / step_length) * len(chunk)
            print(f"Activity: {activity}, Steps: {nr_steps}")

        nr_steps = round(nr_steps)

        print(f"Total steps: {nr_steps}")

        distance_covered = round(nr_steps * step_length)

        print(f"Distance covered: {distance_covered}")

        return nr_steps, distance_covered


    def send_data_to_nodered(self, steps, distance):

        broker = "172.100.10.10"
        port = 1883
        topic = "steps"
        client = mqtt.Client(client_id="publisher")
        client.connect(broker, port)
        client.loop_start()

        data_to_send = {
            "steps": steps,
            "distance": distance
        }

        # Print data to send
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
