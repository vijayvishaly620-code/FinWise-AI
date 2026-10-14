import os
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.dirname(os.path.abspath(__file__))


class FinancialHealthPredictor:
    def __init__(self):
        model_path = os.path.join(ML_DIR, "financial_health_model.pkl")
        encoder_path = os.path.join(ML_DIR, "label_encoder.pkl")
        self.model = None
        self.encoder = None
        if os.path.exists(model_path) and os.path.exists(encoder_path):
            self.model = joblib.load(model_path)
            self.encoder = joblib.load(encoder_path)

    def predict(self, features_dict):
        if self.model is None:
            return {"health": "Unknown", "confidence": 0, "message": "Model not loaded"}
        feature_order = ["monthly_income", "monthly_expenses", "food_spending", "transport_spending",
                         "shopping_spending", "bills", "entertainment", "savings", "debt", "budget_usage"]
        features = np.array([[features_dict.get(f, 0) for f in feature_order]])
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = float(max(probabilities)) * 100
        health_label = self.encoder.inverse_transform([prediction])[0] if self.encoder else str(prediction)
        return {
            "health": health_label,
            "confidence": round(confidence, 1),
            "message": f"Financial health: {health_label} ({confidence:.1f}% confidence)"
        }


class ExpensePredictor:
    def __init__(self):
        model_path = os.path.join(ML_DIR, "expense_predictor.pkl")
        self.model = None
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)

    def predict(self, features_dict):
        if self.model is None:
            return {"predicted": 0, "message": "Model not loaded"}
        feature_order = ["prev_month_expense", "avg_3months", "food", "shopping", "transport", "bills"]
        features = np.array([[features_dict.get(f, 0) for f in feature_order]])
        prediction = self.model.predict(features)[0]
        return {
            "predicted": round(float(prediction), 2),
            "message": f"Predicted next month expense: {prediction:.0f}"
        }
