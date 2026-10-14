import csv
import os
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FOOD_ITEMS = ["Groceries", "Restaurant", "Coffee Shop", "Food Delivery", "Cafeteria", "Street Food", "Bakery", "Juice Bar"]
TRANSPORT_ITEMS = ["Bus", "Metro", "Auto Rickshaw", "Fuel", "Taxi", "Bike Service", "Parking"]
SHOPPING_ITEMS = ["Clothes", "Electronics", "Shoes", "Accessories", "Home Decor", "Books", "Gifts", "Online Shopping"]
BILLS_ITEMS = ["Electricity", "Water", "Internet", "Phone Recharge", "Gas", "DTH", "Insurance"]
EDUCATION_ITEMS = ["Course Fee", "Books", "Stationery", "Online Course", "Exam Fee"]
ENTERTAINMENT_ITEMS = ["Movies", "Streaming", "Games", "Concert", "Sports", "Hobbies"]
HEALTHCARE_ITEMS = ["Doctor Visit", "Medicine", "Gym", "Lab Tests", "Dental"]
RENT_ITEMS = ["House Rent", "Maintenance", "Parking Fee"]
TRAVEL_ITEMS = ["Flight", "Hotel", "Train", "Vacation", "Weekend Trip"]
OTHER_ITEMS = ["Donation", "Pet Care", "Salon", "Miscellaneous"]

INCOME_SOURCES = ["Salary", "Part Time", "Freelance", "Investment", "Business", "Rental", "Gift", "Bonus"]
PAYMENT_METHODS = ["UPI", "Card", "Cash", "Net Banking", "Wallet"]

CATEGORIES = {
    "Food": FOOD_ITEMS,
    "Transport": TRANSPORT_ITEMS,
    "Shopping": SHOPPING_ITEMS,
    "Bills": BILLS_ITEMS,
    "Education": EDUCATION_ITEMS,
    "Entertainment": ENTERTAINMENT_ITEMS,
    "Healthcare": HEALTHCARE_ITEMS,
    "Rent": RENT_ITEMS,
    "Travel": TRAVEL_ITEMS,
    "Other": OTHER_ITEMS,
}

CATEGORY_WEIGHTS = {
    "Food": 0.25,
    "Transport": 0.12,
    "Shopping": 0.15,
    "Bills": 0.15,
    "Education": 0.05,
    "Entertainment": 0.08,
    "Healthcare": 0.05,
    "Rent": 0.10,
    "Travel": 0.03,
    "Other": 0.02,
}

AMOUNT_RANGES = {
    "Food": (50, 800),
    "Transport": (20, 500),
    "Shopping": (100, 3000),
    "Bills": (200, 2000),
    "Education": (100, 5000),
    "Entertainment": (50, 1500),
    "Healthcare": (100, 3000),
    "Rent": (5000, 15000),
    "Travel": (500, 8000),
    "Other": (50, 1000),
}


def generate_users(n=10):
    users = []
    for i in range(1, n + 1):
        uid = f"U{i:03d}"
        income = random.randint(20000, 80000)
        users.append({"id": uid, "income": income})
    return users


def generate_expenses_dataset(users):
    path = os.path.join(BASE_DIR, "expenses_dataset.csv")
    rows = []
    cats = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())
    start_date = datetime(2025, 1, 1)
    for user in users:
        for _ in range(random.randint(40, 70)):
            cat = random.choices(cats, weights=weights, k=1)[0]
            desc = random.choice(CATEGORIES[cat])
            low, high = AMOUNT_RANGES[cat]
            amount = round(random.uniform(low, high), 0)
            days_offset = random.randint(0, 540)
            date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
            rows.append([
                user["id"], date, cat, amount, desc, random.choice(PAYMENT_METHODS)
            ])
    rows.sort(key=lambda x: (x[0], x[1]))
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "date", "category", "amount", "description", "payment_method"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} expense records -> {path}")


def generate_income_dataset(users):
    path = os.path.join(BASE_DIR, "income_dataset.csv")
    rows = []
    start_date = datetime(2025, 1, 1)
    for user in users:
        months = random.randint(12, 18)
        for m in range(months):
            date = (start_date + timedelta(days=m * 30)).strftime("%Y-%m-%d")
            base = user["income"]
            source = random.choice(INCOME_SOURCES[:3])
            amount = base + random.randint(-2000, 5000)
            rows.append([user["id"], date, source, amount, "Monthly"])
            if random.random() < 0.3:
                extra_source = random.choice(INCOME_SOURCES[3:])
                extra_amount = random.randint(1000, 10000)
                extra_date = (start_date + timedelta(days=m * 30 + random.randint(5, 25))).strftime("%Y-%m-%d")
                rows.append([user["id"], extra_date, extra_source, extra_amount, "Irregular"])
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "date", "source", "amount", "income_type"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} income records -> {path}")


def generate_budget_dataset(users):
    path = os.path.join(BASE_DIR, "budget_dataset.csv")
    rows = []
    months = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
              "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
              "2026-01", "2026-02", "2026-03"]
    cats = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Healthcare"]
    budget_pcts = {"Food": 0.20, "Transport": 0.10, "Shopping": 0.12, "Bills": 0.15, "Entertainment": 0.08, "Healthcare": 0.05}
    for user in users:
        for month in months:
            for cat in cats:
                budget = round(user["income"] * budget_pcts[cat] * random.uniform(0.8, 1.2), 0)
                actual = round(budget * random.uniform(0.5, 1.15), 0)
                rows.append([user["id"], month, cat, budget, actual])
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "month", "category", "budget_amount", "actual_amount"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} budget records -> {path}")


def generate_financial_behavior_dataset(n=1000):
    path = os.path.join(BASE_DIR, "financial_behavior_dataset.csv")
    rows = []
    for _ in range(n):
        income = random.randint(15000, 100000)
        expense_pct = random.uniform(0.4, 1.1)
        expenses = round(income * expense_pct, 0)
        food = round(expenses * random.uniform(0.15, 0.30), 0)
        transport = round(expenses * random.uniform(0.08, 0.15), 0)
        shopping = round(expenses * random.uniform(0.08, 0.20), 0)
        bills = round(expenses * random.uniform(0.10, 0.20), 0)
        education = round(expenses * random.uniform(0.02, 0.08), 0)
        entertainment = round(expenses * random.uniform(0.05, 0.12), 0)
        savings = max(0, income - expenses)
        debt = round(random.uniform(0, income * 0.5), 0) if random.random() < 0.3 else 0
        budget_usage = round((expenses / income) * 100, 1) if income > 0 else 100
        savings_rate = round((savings / income) * 100, 1) if income > 0 else 0
        if savings_rate >= 20 and budget_usage <= 80:
            health = "Excellent"
        elif savings_rate >= 10 and budget_usage <= 90:
            health = "Good"
        elif savings_rate >= 5 or budget_usage <= 100:
            health = "Average"
        else:
            health = "Poor"
        noise = random.uniform(-3, 3)
        savings_rate = round(max(0, savings_rate + noise), 1)
        rows.append([
            income, expenses, food, transport, shopping, bills, education,
            entertainment, savings, debt, budget_usage, savings_rate, health
        ])
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "monthly_income", "monthly_expenses", "food_spending", "transport_spending",
            "shopping_spending", "bills", "education", "entertainment", "savings",
            "debt", "budget_usage", "savings_rate", "financial_health"
        ])
        writer.writerows(rows)
    print(f"Generated {len(rows)} financial behavior records -> {path}")


if __name__ == "__main__":
    print("Generating datasets...")
    users = generate_users(10)
    generate_expenses_dataset(users)
    generate_income_dataset(users)
    generate_budget_dataset(users)
    generate_financial_behavior_dataset(1000)
    print("\nAll datasets generated successfully!")
