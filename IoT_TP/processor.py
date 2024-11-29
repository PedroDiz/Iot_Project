class Processor:
    def __init__(self, db):
        self.db = db

    def process_message(self, topic, payload):
        try:
            id = topic.split("/")[1]

            if topic.endswith("/static"):
                self._process_static_data(id, payload)
            else:
                self._process_movement_data(id, payload)

        except Exception as e:
            print(f"Error processing message: {e}")

    def _process_static_data(self, id, data):
        self.db.insert_person(
            id=id,
            weight=data["bodyweight"],
            height=data["height"],
            age=data["age"]
        )

    def _process_movement_data(self, id, data):
        self.db.insert_movement(
            id=id,
            acceleration_x=data["acceleration_x"],
            acceleration_y=data["acceleration_y"],
            acceleration_z=data["acceleration_z"],
            gyro_x=data["gyro_x"],
            gyro_y=data["gyro_y"],
            gyro_z=data["gyro_z"],
            movement_data=data["date"],
            movement_time=data["time"]
        )
