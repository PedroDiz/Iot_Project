import pandas as pd
from mlprocessor import MLProcessor

def main():

    ml_processor = MLProcessor("activity_model.pkl", "scaler.pkl")

    # New data to predict (fix by using a DataFrame)
    columns = ['acceleration_x', 'acceleration_y', 'acceleration_z', 'gyro_x', 'gyro_y', 'gyro_z']
    new_data = [[0.2650, -0.7814, -0.0076, -0.0590, 0.0325, -2.9296]]
    new_data_df = pd.DataFrame(new_data, columns=columns)

    activity = ml_processor.predict_activity(new_data_df)
    print(f"Predicted activity: {activity}")

if __name__ == "__main__":
    main()