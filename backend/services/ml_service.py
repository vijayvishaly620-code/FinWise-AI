import os
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "ml")
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

HEALTH_FEATURES = [
    "monthly_income", "monthly_expenses", "food_expense", "transport_expense",
    "shopping_expense", "bill_expense", "education_expense", "entertainment_expense",
    "healthcare_expense", "rent_expense", "travel_expense", "other_expense",
    "monthly_savings", "existing_debt", "budget_amount", "budget_used_percentage",
    "savings_rate", "expense_ratio", "goal_progress", "credit_score"
]

EXPENSE_FEATURES = [
    "monthly_income", "food_expense", "transport_expense", "shopping_expense",
    "bill_expense", "education_expense", "entertainment_expense",
    "healthcare_expense", "rent_expense", "travel_expense", "other_expense"
]


class MLPredictor:
    def __init__(self):
        health_path = os.path.join(ML_DIR, "financial_health_model.pkl")
        encoder_path = os.path.join(ML_DIR, "label_encoder.pkl")
        expense_path = os.path.join(ML_DIR, "expense_prediction_model.pkl")

        self.health_model = None
        self.encoder = None
        self.expense_model = None
        self.available = False

        if os.path.exists(health_path) and os.path.exists(encoder_path):
            self.health_model = joblib.load(health_path)
            self.encoder = joblib.load(encoder_path)

        if os.path.exists(expense_path):
            self.expense_model = joblib.load(expense_path)

        if self.health_model and self.encoder:
            self.available = True

    def predict_health(self, user_data):
        if not self.health_model or not self.encoder:
            return {"health": "Unknown", "confidence": 0, "message": "Health model not loaded. Run train_model.py first."}
        try:
            cats = user_data.get("categories", {})
            income = user_data.get("monthlyIncome", 0) or user_data.get("totalIncome", 0)
            expenses = user_data.get("totalExpenses", 0)
            savings = income - expenses
            savings_rate = (savings / income * 100) if income > 0 else 0
            expense_ratio = (expenses / income * 100) if income > 0 else 0

            features = np.array([[
                income, expenses,
                cats.get("Food", 0), cats.get("Transport", 0),
                cats.get("Shopping", 0), cats.get("Bills", 0),
                cats.get("Education", 0), cats.get("Entertainment", 0),
                cats.get("Healthcare", 0), cats.get("Rent", 0),
                cats.get("Travel", 0), cats.get("Other", 0),
                savings, 0,
                income * 0.9,
                (expenses / (income * 0.9) * 100) if income > 0 else 0,
                savings_rate, expense_ratio,
                50, 700
            ]])

            prediction = self.health_model.predict(features)[0]
            probabilities = self.health_model.predict_proba(features)[0]
            confidence = float(max(probabilities)) * 100
            health_label = self.encoder.inverse_transform([prediction])[0] if self.encoder else str(prediction)

            return {
                "health": health_label,
                "confidence": round(confidence, 1),
                "message": f"ML prediction: Your financial health is '{health_label}' ({confidence:.1f}% confidence)."
            }
        except Exception as e:
            return {"health": "Unknown", "confidence": 0, "message": f"Prediction error: {str(e)}"}

    def predict_expenses(self, user_data):
        if not self.expense_model:
            return {"predicted": 0, "message": "Expense model not loaded. Run train_model.py first."}
        try:
            cats = user_data.get("categories", {})
            income = user_data.get("monthlyIncome", 0) or user_data.get("totalIncome", 0)

            features = np.array([[
                income,
                cats.get("Food", 0), cats.get("Transport", 0),
                cats.get("Shopping", 0), cats.get("Bills", 0),
                cats.get("Education", 0), cats.get("Entertainment", 0),
                cats.get("Healthcare", 0), cats.get("Rent", 0),
                cats.get("Travel", 0), cats.get("Other", 0)
            ]])

            prediction = self.expense_model.predict(features)[0]
            return {
                "predicted": round(float(prediction), 2),
                "message": f"Estimated next month expense: {prediction:,.0f}"
            }
        except Exception as e:
            return {"predicted": 0, "message": f"Prediction error: {str(e)}"}

    def get_dataset_info(self):
        import pandas as pd
        csv_path = os.path.join(DATASETS_DIR, "financial_dataset.csv")
        if not os.path.exists(csv_path):
            return None
        df = pd.read_csv(csv_path)
        return {
            "name": "Financial Dataset",
            "records": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "missing_values": int(df.isnull().sum().sum()),
            "numeric_stats": {
                "income_mean": round(float(df["monthly_income"].mean()), 0),
                "income_min": int(df["monthly_income"].min()),
                "income_max": int(df["monthly_income"].max()),
                "expense_mean": round(float(df["monthly_expenses"].mean()), 0),
                "savings_mean": round(float(df["monthly_savings"].mean()), 0),
                "savings_rate_mean": round(float(df["savings_rate"].mean()), 1),
                "expense_ratio_mean": round(float(df["expense_ratio"].mean()), 1),
            },
            "health_distribution": df["financial_health"].value_counts().to_dict(),
            "employment_distribution": df["employment_type"].value_counts().to_dict(),
            "goal_distribution": df["financial_goal"].value_counts().to_dict(),
            "preview": df.head(10).to_dict(orient="records"),
        }
