"""
FinWise AI - ML Model Training
Trains Financial Health Classifier and Expense Predictor
Uses financial_dataset.csv (2000 records)
"""
import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
ML_DIR = os.path.dirname(os.path.abspath(__file__))


def train_health_model():
    print("=" * 60)
    print("MODEL 1: Financial Health Classification (RandomForestClassifier)")
    print("=" * 60)
    csv_path = os.path.join(DATASETS_DIR, "financial_dataset.csv")
    if not os.path.exists(csv_path):
        print(f"Dataset not found at {csv_path}")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    print(f"Dataset loaded: {len(df)} records, {len(df.columns)} columns")

    print(f"\nFinancial Health distribution:")
    print(df["financial_health"].value_counts().to_string())

    features = [
        "monthly_income", "monthly_expenses", "food_expense", "transport_expense",
        "shopping_expense", "bill_expense", "education_expense", "entertainment_expense",
        "healthcare_expense", "rent_expense", "travel_expense", "other_expense",
        "monthly_savings", "existing_debt", "budget_amount", "budget_used_percentage",
        "savings_rate", "expense_ratio", "goal_progress", "credit_score"
    ]

    X = df[features].fillna(0)
    y = df["financial_health"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=15, min_samples_split=5, min_samples_leaf=2)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    print(f"Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    labels = le.classes_
    print(f"{'':>20s}", end="")
    for label in labels:
        print(f"{label:>18s}", end="")
    print()
    for i, row in enumerate(cm):
        print(f"{labels[i]:>20s}", end="")
        for val in row:
            print(f"{val:>18d}", end="")
        print()

    model_path = os.path.join(ML_DIR, "financial_health_model.pkl")
    encoder_path = os.path.join(ML_DIR, "label_encoder.pkl")
    joblib.dump(model, model_path)
    joblib.dump(le, encoder_path)
    print(f"\nModel saved: {model_path}")
    print(f"Encoder saved: {encoder_path}")

    importances = model.feature_importances_
    print(f"\nTop 10 Feature Importances:")
    for feat, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {feat:>25s}: {imp:.4f}")

    return accuracy


def train_expense_model():
    print("\n" + "=" * 60)
    print("MODEL 2: Expense Prediction (RandomForestRegressor)")
    print("=" * 60)
    csv_path = os.path.join(DATASETS_DIR, "financial_dataset.csv")
    df = pd.read_csv(csv_path)
    print(f"Dataset loaded: {len(df)} records")

    features = [
        "monthly_income", "food_expense", "transport_expense", "shopping_expense",
        "bill_expense", "education_expense", "entertainment_expense",
        "healthcare_expense", "rent_expense", "travel_expense", "other_expense"
    ]
    target = "monthly_expenses"

    X = df[features].fillna(0)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    model = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=15, min_samples_split=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"  MAE:  {mae:,.2f}")
    print(f"  RMSE: {rmse:,.2f}")
    print(f"  R2:   {r2:.4f}")

    model_path = os.path.join(ML_DIR, "expense_prediction_model.pkl")
    joblib.dump(model, model_path)
    print(f"\nModel saved: {model_path}")

    importances = model.feature_importances_
    print(f"\nFeature Importances:")
    for feat, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True):
        print(f"  {feat:>25s}: {imp:.4f}")

    return r2


if __name__ == "__main__":
    acc = train_health_model()
    r2 = train_expense_model()
    print("\n" + "=" * 60)
    print("ALL MODELS TRAINED SUCCESSFULLY")
    print(f"  Health Model Accuracy: {acc*100:.2f}%")
    print(f"  Expense Model R2: {r2:.4f}")
    print("=" * 60)
