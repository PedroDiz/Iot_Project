from mlprocessor import MLProcessor
from modelinitializer import ModelInitializer
import pandas as pd

columns = ['acceleration_x', 'acceleration_y', 'acceleration_z', 'gyro_x', 'gyro_y', 'gyro_z']
file_load = "training.txt"
model_save = "model.pkl"
scaler_save = "scaler.pkl"

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
