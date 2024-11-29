from mlprocessor import MLProcessor
from modelinitializer import ModelInitializer
import pandas as pd

columns = ['acceleration_x', 'acceleration_y', 'acceleration_z', 'gyro_x', 'gyro_y', 'gyro_z']
file_load = "training.txt"
model_save = "model.pkl"
scaler_save = "scaler.pkl"

velocity_map = {
    range(20, 30): {"male": 1.36, "female": 1.34},
    range(30, 40): {"male": 1.43, "female": 1.34},
    range(40, 50): {"male": 1.45, "female": 1.39},
    range(50, 60): {"male": 1.43, "female": 1.31},
    range(60, 70): {"male": 1.34, "female": 1.24},
    range(70, 80): {"male": 1.26, "female": 1.13},
    range(80, 90): {"male": 0.97, "female": 0.94},
}


class Processor:
    def __init__(self, db):
        self.db = db
        model_initializer = ModelInitializer(file_load, model_save, scaler_save)
        model_initializer.build_model()
        self.ml_processor = MLProcessor(model_save, scaler_save)

    def process_message(self, topic, payload):
        try:
            id = topic.split("/")[1]
            if topic.endswith("/static"):
                self._process_static_data(id, payload)
            else:
                movement_data = self.extract_movement_parameters(payload)
                data_to_process = pd.DataFrame([movement_data], columns=columns)
                activity = int(self.ml_processor.predict_activity(data_to_process))
                self._process_movement_data(id, activity, payload)

        except Exception as e:
            print(f"Error processing message: {e}")

    def _process_static_data(self, id, data):
        self.db.insert_person(
            id=id,
            weight=data["bodyweight"],
            height=data["height"],
            age=data["age"]
        )

    def _process_movement_data(self, id, activity, data):
        self.db.insert_movement(
            id=id,
            acceleration_x=data["acceleration_x"],
            acceleration_y=data["acceleration_y"],
            acceleration_z=data["acceleration_z"],
            gyro_x=data["gyro_x"],
            gyro_y=data["gyro_y"],
            gyro_z=data["gyro_z"],
            movement_data=data["date"],
            movement_time=data["time"],
            activity = activity
        )

    def extract_movement_parameters(self, data):
        return [
            data["acceleration_x"],
            data["acceleration_y"],
            data["acceleration_z"],
            data["gyro_x"],
            data["gyro_y"],
            data["gyro_z"]
        ]

    def calculate_burnt_calories(self, age, gender, weight, height, activity):
        for age_range, genders in velocity_map.items():
            if age in age_range:
                velocity = genders.get(gender)
                break

        if activity == 1:
            velocity*=2

        return 0.035 * weight + ((velocity ** 2)/height) * 0.029 * weight

