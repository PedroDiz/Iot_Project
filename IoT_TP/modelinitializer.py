import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


class ModelInitializer:
    def __init__(self, text_file, model_path, scaler_path):
        self.text_file = text_file
        self.model_path = model_path
        self.scaler_path = scaler_path

    def build_model(self):
        # Load data
        data = pd.read_csv(self.text_file, delimiter=";")

        # Features and labels
        X = data[['acceleration_x', 'acceleration_y', 'acceleration_z', 'gyro_x', 'gyro_y', 'gyro_z']]
        y = data['activity']

        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Split data into training and testing sets, 70-30 split
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

        # Initialize the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)

        # Train the model
        model.fit(X_train, y_train)

        # Test the model
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")
        print(classification_report(y_test, y_pred))

        # Save the model and scaler

        joblib.dump(model, self.model_path)
        joblib.dump(scaler, self.scaler_path)