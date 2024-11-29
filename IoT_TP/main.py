import pandas as pd
from mlprocessor import MLProcessor
from repository import MovementDatabase

repo = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")

def main():
    repo.insert_person(64852, 25, 70, 180)

    repo.insert_movement(
        id=64852,
        acceleration_x=0.1,
        acceleration_y=0.2,
        acceleration_z=0.3,
        gyro_x=0.4,
        gyro_y=0.5,
        gyro_z=0.6,
        movement_data="2021-01-01",
        movement_time="12:00:00",
        activity=0
    )

if __name__ == "__main__":
    main()