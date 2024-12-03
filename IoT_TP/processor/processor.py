from mlprocessor import MLProcessor
from modelinitializer import ModelInitializer
import pandas as pd

from processors import ActivityTimeProcessor, CaloriesProcessor, StepProcessor

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
        self.calories_processor = CaloriesProcessor()
        self.steps_processor = StepProcessor()
        self.activity_time_processor = ActivityTimeProcessor()
        self.person_data = db.retrieve_person(64852)
        movement_data = db.retrieve_movement(64852)
        self.movement_data = self.exclude_ids_from_movement_data(movement_data)
        self.process_all()

    def process_message(self, topic, payload):
        try:
            id = topic.split("/")[1]
            if topic.endswith("/static"):
                self.store_static_data(id, payload)
            else:
                movement_data = self.extract_movement_parameters(payload)
                data_to_process = pd.DataFrame([movement_data], columns=columns)
                activity = int(self.ml_processor.predict_activity(data_to_process))
                self.store_movement_data(id, activity, payload)
                self.process_all()

        except Exception as e:
            print(f"Error processing message: {e}")

    def process_all(self):
        if not self.person_data or not self.movement_data:
            return
        # Process the data
        steps, distance_covered = self.steps_processor.process(self.person_data, self.movement_data)
        calories_burned = self.calories_processor.process(self.person_data, self.movement_data)
        activity_time = self.activity_time_processor.process(self.movement_data)

        # Send the data to Node-RED
        self.steps_processor.send_data_to_nodered(steps, distance_covered)
        self.calories_processor.send_data_to_nodered(calories_burned)
        self.activity_time_processor.send_data_to_nodered(activity_time)

    def store_static_data(self, id, data):
        self.db.insert_person(
            id=id,
            gender=data["gender"],
            weight=data["bodyweight"],
            height=data["height"],
            age=data["age"]
        )

        self.person_data = [id, data["age"], data["gender"], data["bodyweight"], data["height"]]

    def store_movement_data(self, id, activity, data):
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

        movement_entry = (
            activity, data["acceleration_x"], data["acceleration_y"], data["acceleration_z"],
            data["gyro_x"], data["gyro_y"], data["gyro_z"], data["date"], data["time"]
        )
        self.movement_data.append(movement_entry)

    def extract_movement_parameters(self, data):
        return [
            data["acceleration_x"],
            data["acceleration_y"],
            data["acceleration_z"],
            data["gyro_x"],
            data["gyro_y"],
            data["gyro_z"]
        ]

    def exclude_ids_from_movement_data(self, movement_data):
        return [record[2:] for record in movement_data]

