import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")


def load_and_clean(dataset_name):
    csv_path = os.path.join(DATASETS_DIR, dataset_name)
    if not os.path.exists(csv_path):
        print(f"Dataset not found: {csv_path}")
        return None
    df = pd.read_csv(csv_path)
    print(f"Loaded {dataset_name}: {len(df)} rows, {len(df.columns)} columns")
    print(f"Missing values:\n{df.isnull().sum()}")
    df = df.dropna()
    print(f"After cleaning: {len(df)} rows")
    return df


def preprocess_behavior_data():
    df = load_and_clean("financial_behavior_dataset.csv")
    if df is None:
        return None
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.01)
        q99 = df[col].quantile(0.99)
        df = df[(df[col] >= q1) & (df[col] <= q99)]
    print(f"After outlier removal: {len(df)} rows")
    return df


if __name__ == "__main__":
    print("Preprocessing datasets...")
    for name in ["expenses_dataset.csv", "income_dataset.csv", "budget_dataset.csv", "financial_behavior_dataset.csv"]:
        df = load_and_clean(name)
        if df is not None:
            print(f"  {name}: {len(df)} clean records")
