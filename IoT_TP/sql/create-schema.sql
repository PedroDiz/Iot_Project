CREATE TABLE Movement (
    movement_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    acceleration_x FLOAT,
    acceleration_y FLOAT,
    acceleration_z FLOAT,
    gyro_x FLOAT,
    gyro_y FLOAT,
    gyro_z FLOAT,
    movement_data VARCHAR(10),
    movement_time VARCHAR(8)
);