from repository import MovementDatabase

db = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")

def main():

    # Retrieve Person
    person = db.retrieve_person(64852)
    print(f"Person: {person}")

    # Retrieve rows
    rows = db.retrieve_movement(64852)
    for row in rows:
        print(f"MOV_ID: {row[0]}, USER_ID: {row[1]} Accel_X: {row[2]}, Accel_Y: {row[3]}, Accel_Z: {row[4]}, "
              f"Gyro_X: {row[5]}, Gyro_Y: {row[6]}, Gyro_Z: {row[7]}, "
              f"Date: {row[8]}, Time: {row[9]}")

if __name__ == "__main__":
    main()