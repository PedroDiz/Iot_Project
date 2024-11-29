import joblib

class MLProcessor:
    def __init__(self, model_path, scaler_path):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict_activity(self, data):
        try:
            data_scaled = self.scaler.transform(data)
            activity = self.model.predict(data_scaled)
            return activity[0]
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
