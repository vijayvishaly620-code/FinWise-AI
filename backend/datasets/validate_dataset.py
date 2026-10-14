"""Validates financial_dataset.csv"""
import os
import pandas as pd
import sys

REQUIRED_COLUMNS = [
    "user_id", "age", "employment_type", "monthly_income", "monthly_expenses",
    "food_expense", "transport_expense", "shopping_expense", "bill_expense",
    "education_expense", "entertainment_expense", "healthcare_expense",
    "rent_expense", "travel_expense", "other_expense", "monthly_savings",
    "existing_debt", "budget_amount", "budget_used_percentage", "savings_rate",
    "expense_ratio", "financial_goal", "goal_amount", "goal_progress",
    "credit_score", "financial_health"
]
VALID_HEALTH = ["Poor", "Needs Improvement", "Good", "Excellent"]
VALID_EMPLOYMENT = ["Student", "Employee", "Self-Employed", "Freelancer", "Business Owner"]
EXPECTED_RECORDS = 2000


def validate():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "financial_dataset.csv")
    if not os.path.exists(csv_path):
        print("FAIL: financial_dataset.csv not found")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    errors = []
    warnings = []

    if len(df) != EXPECTED_RECORDS:
        errors.append(f"Row count: expected {EXPECTED_RECORDS}, got {len(df)}")

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")

    dup_ids = df["user_id"].duplicated().sum()
    if dup_ids > 0:
        errors.append(f"Duplicate user IDs: {dup_ids}")

    missing_vals = df.isnull().sum().sum()
    if missing_vals > 0:
        errors.append(f"Missing values: {missing_vals}")

    if (df["monthly_income"] <= 0).any():
        errors.append("Non-positive monthly_income found")
    if (df["monthly_expenses"] <= 0).any():
        errors.append("Non-positive monthly_expenses found")

    calc_savings = df["monthly_income"] - df["monthly_expenses"]
    mismatched = (df["monthly_savings"].round(0) != calc_savings.round(0)).sum()
    if mismatched > 0:
        warnings.append(f"monthly_savings mismatches: {mismatched}")

    if (df["savings_rate"] < 0).any() or (df["savings_rate"] > 100).any():
        errors.append("savings_rate out of 0-100 range")

    if (df["expense_ratio"] < 0).any():
        errors.append("Negative expense_ratio found")

    invalid_health = df[~df["financial_health"].isin(VALID_HEALTH)]
    if len(invalid_health) > 0:
        errors.append(f"Invalid financial_health values: {df['financial_health'].unique().tolist()}")

    invalid_emp = df[~df["employment_type"].isin(VALID_EMPLOYMENT)]
    if len(invalid_emp) > 0:
        errors.append(f"Invalid employment_type values: {df['employment_type'].unique().tolist()}")

    if errors:
        print("Dataset Validation FAILED\n")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)

    print("Dataset Validation Successful\n")
    print(f"Records: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Missing Values: {missing_vals}")
    print(f"Duplicate Records: {dup_ids}")
    print(f"Invalid Records: 0")
    if warnings:
        print(f"\nWarnings:")
        for w in warnings:
            print(f"  WARN: {w}")
    print(f"\nHealth distribution:")
    print(df["financial_health"].value_counts().to_string())
    print(f"\nEmployment distribution:")
    print(df["employment_type"].value_counts().to_string())
    print(f"\nIncome range: {df['monthly_income'].min():.0f} - {df['monthly_income'].max():.0f}")
    print(f"Mean savings rate: {df['savings_rate'].mean():.1f}%")
    print(f"Mean expense ratio: {df['expense_ratio'].mean():.1f}%")


if __name__ == "__main__":
    validate()
