"""
FinWise AI - Financial Dataset Generator
Generates exactly 2,000 synthetic financial records for ML training.
Seed = 42 for reproducibility.
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N_RECORDS = 2000

np.random.seed(SEED)

EMPLOYMENT_TYPES = ["Student", "Employee", "Self-Employed", "Freelancer", "Business Owner"]
EMPLOYMENT_WEIGHTS = [0.15, 0.40, 0.20, 0.15, 0.10]
EMPLOYMENT_INCOME_RANGE = {
    "Student": (5000, 25000),
    "Employee": (20000, 120000),
    "Self-Employed": (15000, 150000),
    "Freelancer": (10000, 100000),
    "Business Owner": (30000, 300000),
}
FINANCIAL_GOALS = ["Emergency Fund", "New Laptop", "New Phone", "Bike", "Car", "Education", "Travel", "House", "Business", "Higher Studies"]
GOAL_AMOUNTS = {
    "Emergency Fund": (50000, 300000),
    "New Laptop": (30000, 120000),
    "New Phone": (10000, 50000),
    "Bike": (50000, 200000),
    "Car": (300000, 1500000),
    "Education": (100000, 500000),
    "Travel": (30000, 200000),
    "House": (500000, 2000000),
    "Business": (100000, 1000000),
    "Higher Studies": (200000, 800000),
}
GOAL_WEIGHTS = [0.15, 0.10, 0.12, 0.08, 0.12, 0.10, 0.08, 0.10, 0.08, 0.07]


def generate_dataset():
    print("Generating 2,000 synthetic financial records...")
    print(f"Random seed: {SEED}\n")

    user_ids = [f"U{i:04d}" for i in range(1, N_RECORDS + 1)]
    ages = np.random.randint(18, 61, N_RECORDS)
    employment_types = np.random.choice(EMPLOYMENT_TYPES, N_RECORDS, p=EMPLOYMENT_WEIGHTS)

    monthly_incomes = np.zeros(N_RECORDS)
    for i in range(N_RECORDS):
        emp = employment_types[i]
        low, high = EMPLOYMENT_INCOME_RANGE[emp]
        monthly_incomes[i] = np.random.randint(low, high)

    monthly_incomes = np.round(monthly_incomes, -2)

    expense_ratios = np.clip(np.random.normal(0.72, 0.15, N_RECORDS), 0.30, 1.15)
    monthly_expenses = np.round(monthly_incomes * expense_ratios, -1)
    monthly_expenses = np.minimum(monthly_expenses, monthly_incomes * 1.2)

    food_pct = np.random.uniform(0.12, 0.30, N_RECORDS)
    transport_pct = np.random.uniform(0.05, 0.15, N_RECORDS)
    shopping_pct = np.random.uniform(0.05, 0.20, N_RECORDS)
    bill_pct = np.random.uniform(0.08, 0.18, N_RECORDS)
    edu_pct = np.random.uniform(0.02, 0.10, N_RECORDS)
    entertain_pct = np.random.uniform(0.03, 0.12, N_RECORDS)
    health_pct = np.random.uniform(0.02, 0.08, N_RECORDS)
    rent_pct = np.random.uniform(0.00, 0.25, N_RECORDS)
    travel_pct = np.random.uniform(0.01, 0.08, N_RECORDS)

    total_pcts = food_pct + transport_pct + shopping_pct + bill_pct + edu_pct + entertain_pct + health_pct + rent_pct + travel_pct
    food_pct /= total_pcts
    transport_pct /= total_pcts
    shopping_pct /= total_pcts
    bill_pct /= total_pcts
    edu_pct /= total_pcts
    entertain_pct /= total_pcts
    health_pct /= total_pcts
    rent_pct /= total_pcts
    travel_pct /= total_pcts
    other_pct = 1.0 - (food_pct + transport_pct + shopping_pct + bill_pct + edu_pct + entertain_pct + health_pct + rent_pct + travel_pct)

    food_expense = np.round(monthly_expenses * food_pct, -1)
    transport_expense = np.round(monthly_expenses * transport_pct, -1)
    shopping_expense = np.round(monthly_expenses * shopping_pct, -1)
    bill_expense = np.round(monthly_expenses * bill_pct, -1)
    education_expense = np.round(monthly_expenses * edu_pct, -1)
    entertainment_expense = np.round(monthly_expenses * entertain_pct, -1)
    healthcare_expense = np.round(monthly_expenses * health_pct, -1)
    rent_expense = np.round(monthly_expenses * rent_pct, -1)
    travel_expense = np.round(monthly_expenses * travel_pct, -1)
    other_expense = np.round(monthly_expenses * np.maximum(other_pct, 0.01), -1)

    monthly_savings = monthly_incomes - monthly_expenses
    monthly_savings = np.maximum(monthly_savings, 0)

    debt_prob = np.where(employment_types == "Student", 0.5, 0.3)
    has_debt = np.random.random(N_RECORDS) < debt_prob
    existing_debt = np.where(
        has_debt,
        np.round(np.random.uniform(10000, 1000000, N_RECORDS) / 1000) * 10,
        0
    )

    budget_amount = np.round(monthly_incomes * np.random.uniform(0.85, 1.10, N_RECORDS), -2)
    budget_used_pct = np.round((monthly_expenses / budget_amount) * 100, 1)
    budget_used_pct = np.clip(budget_used_pct, 20, 130)

    savings_rate = np.round((monthly_savings / monthly_incomes) * 100, 1)
    savings_rate = np.clip(savings_rate, 0, 80)
    expense_ratio = np.round((monthly_expenses / monthly_incomes) * 100, 1)

    goals = np.random.choice(FINANCIAL_GOALS, N_RECORDS, p=GOAL_WEIGHTS)
    goal_amounts = np.zeros(N_RECORDS)
    for i in range(N_RECORDS):
        low, high = GOAL_AMOUNTS[goals[i]]
        goal_amounts[i] = np.round(np.random.randint(low, high) / 1000) * 10
    goal_progress = np.round(np.random.beta(2, 3, N_RECORDS) * 100, 1)
    goal_progress = np.clip(goal_progress, 0, 100)

    credit_scores = np.clip(
        np.round(np.random.normal(680, 120, N_RECORDS)),
        300, 900
    ).astype(int)

    health_scores = np.zeros(N_RECORDS, dtype=float)
    for i in range(N_RECORDS):
        score = 50
        sr = savings_rate[i]
        if sr >= 25:
            score += 20
        elif sr >= 15:
            score += 12
        elif sr >= 5:
            score += 5
        else:
            score -= 8
        er = expense_ratio[i]
        if er <= 60:
            score += 15
        elif er <= 80:
            score += 8
        elif er <= 100:
            score += 0
        else:
            score -= 10
        bu = budget_used_pct[i]
        if bu <= 80:
            score += 10
        elif bu <= 100:
            score += 5
        else:
            score -= 8
        if existing_debt[i] == 0:
            score += 8
        elif existing_debt[i] < monthly_incomes[i] * 6:
            score += 3
        else:
            score -= 5
        gp = goal_progress[i]
        score += int(gp / 20)
        cs = credit_scores[i]
        if cs >= 750:
            score += 5
        elif cs >= 650:
            score += 2
        else:
            score -= 3
        if employment_types[i] == "Student":
            score += 2
        age = ages[i]
        if 25 <= age <= 45:
            score += 2
        noise = np.random.uniform(-4, 4)
        score += noise
        health_scores[i] = np.clip(score, 0, 100)

    financial_health = []
    for s in health_scores:
        if s >= 80:
            financial_health.append("Excellent")
        elif s >= 60:
            financial_health.append("Good")
        elif s >= 40:
            financial_health.append("Needs Improvement")
        else:
            financial_health.append("Poor")

    df = pd.DataFrame({
        "user_id": user_ids,
        "age": ages,
        "employment_type": employment_types,
        "monthly_income": monthly_incomes.astype(int),
        "monthly_expenses": monthly_expenses.astype(int),
        "food_expense": food_expense.astype(int),
        "transport_expense": transport_expense.astype(int),
        "shopping_expense": shopping_expense.astype(int),
        "bill_expense": bill_expense.astype(int),
        "education_expense": education_expense.astype(int),
        "entertainment_expense": entertainment_expense.astype(int),
        "healthcare_expense": healthcare_expense.astype(int),
        "rent_expense": rent_expense.astype(int),
        "travel_expense": travel_expense.astype(int),
        "other_expense": other_expense.astype(int),
        "monthly_savings": monthly_savings.astype(int),
        "existing_debt": existing_debt.astype(int),
        "budget_amount": budget_amount.astype(int),
        "budget_used_percentage": budget_used_pct,
        "savings_rate": savings_rate,
        "expense_ratio": expense_ratio,
        "financial_goal": goals,
        "goal_amount": goal_amounts.astype(int),
        "goal_progress": goal_progress,
        "credit_score": credit_scores,
        "financial_health": financial_health,
    })

    df = df.drop_duplicates()
    if len(df) != N_RECORDS:
        raise ValueError(f"Expected {N_RECORDS} records, got {len(df)}")

    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "financial_dataset.csv")
    df.to_csv(output_path, index=False)

    print("Dataset generated successfully.")
    print(f"Total records: {len(df)}")
    print(f"File: financial_dataset.csv")
    print(f"\nColumn summary:")
    print(f"  Numeric columns: {len(df.select_dtypes(include=[np.number]).columns)}")
    print(f"  Categorical columns: {len(df.select_dtypes(include=['object']).columns)}")
    print(f"\nFinancial health distribution:")
    print(df["financial_health"].value_counts().to_string())
    print(f"\nEmployment type distribution:")
    print(df["employment_type"].value_counts().to_string())
    print(f"\nIncome range: ₹{df['monthly_income'].min():,.0f} – ₹{df['monthly_income'].max():,.0f}")
    print(f"Mean income: ₹{df['monthly_income'].mean():,.0f}")
    print(f"Mean savings rate: {df['savings_rate'].mean():.1f}%")
    print(f"Mean expense ratio: {df['expense_ratio'].mean():.1f}%")


if __name__ == "__main__":
    generate_dataset()
