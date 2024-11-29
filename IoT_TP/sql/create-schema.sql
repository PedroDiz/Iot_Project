CREATE TABLE Person(
    person_id INT PRIMARY KEY,
    age INT NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL
);

CREATE TABLE Movement (
    movement_id SERIAL,
    user_id INT references Person(person_id),
    activity_number INT,
    acceleration_x FLOAT,
    acceleration_y FLOAT,
    acceleration_z FLOAT,
    gyro_x FLOAT,
    gyro_y FLOAT,
    gyro_z FLOAT,
    movement_data VARCHAR(10) NOT NULL,
    movement_time VARCHAR(8) NOT NULL,
    PRIMARY KEY (user_id, movement_id)
);