"""
FinWise AI - Demo Account Seeder
Run this script to create a demo account with realistic sample data.

Usage: python seed_demo.py
"""

import os
import sys
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from werkzeug.security import generate_password_hash

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/finwise_ai")

FOOD_ITEMS = ["Groceries", "Restaurant", "Coffee Shop", "Food Delivery", "Cafeteria", "Bakery"]
TRANSPORT_ITEMS = ["Bus Pass", "Metro Card", "Auto Rickshaw", "Fuel", "Uber"]
SHOPPING_ITEMS = ["Clothes", "Electronics", "Shoes", "Online Shopping", "Home Decor"]
BILLS_ITEMS = ["Electricity Bill", "Internet Bill", "Phone Recharge", "Gas Bill", "Water Bill"]
EDUCATION_ITEMS = ["Course Fee", "Books", "Online Course"]
ENTERTAINMENT_ITEMS = ["Movies", "Netflix", "Concert", "Games"]
HEALTHCARE_ITEMS = ["Doctor Visit", "Medicine", "Gym Membership"]
RENT_ITEMS = ["House Rent", "Maintenance"]
TRAVEL_ITEMS = ["Weekend Trip", "Train Ticket"]
OTHER_ITEMS = ["Salon", "Donation", "Miscellaneous"]

CATEGORY_ITEMS = {
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

CATEGORY_AMOUNTS = {
    "Food": (150, 600),
    "Transport": (50, 400),
    "Shopping": (200, 2500),
    "Bills": (300, 1800),
    "Education": (200, 3000),
    "Entertainment": (100, 1200),
    "Healthcare": (200, 2500),
    "Rent": (8000, 12000),
    "Travel": (500, 4000),
    "Other": (100, 800),
}

CATEGORY_WEIGHTS = {
    "Food": 0.25,
    "Transport": 0.10,
    "Shopping": 0.12,
    "Bills": 0.15,
    "Education": 0.05,
    "Entertainment": 0.08,
    "Healthcare": 0.05,
    "Rent": 0.12,
    "Travel": 0.03,
    "Other": 0.05,
}

PAYMENT_METHODS = ["UPI", "Card", "Cash", "Net Banking", "Wallet"]


def seed():
    print("Connecting to MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client.get_database()

    print("Clearing existing demo data...")
    demo_user = db.users.find_one({"email": "demo@finwise.ai"})
    if demo_user:
        user_id = str(demo_user["_id"])
        db.transactions.delete_many({"userId": user_id})
        db.budgets.delete_many({"userId": user_id})
        db.savings_goals.delete_many({"userId": user_id})
        db.alerts.delete_many({"userId": user_id})
        db.users.delete_one({"_id": demo_user["_id"]})
        print("Existing demo account removed.")

    print("Creating demo user...")
    user_doc = {
        "fullName": "Demo User",
        "email": "demo@finwise.ai",
        "password": generate_password_hash("Demo@123"),
        "monthlyIncome": 50000,
        "currency": "INR",
        "financialGoal": "Build emergency fund and save for a car",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    result = db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)
    print(f"Demo user created with ID: {user_id}")

    print("Generating transactions...")
    cats = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())
    now = datetime.now()

    for months_ago in range(6, -1, -1):
        month_date = now - timedelta(days=months_ago * 30)
        year = month_date.year
        month = month_date.month

        income_doc = {
            "userId": user_id,
            "type": "income",
            "amount": 50000 + random.randint(-2000, 5000),
            "category": "Income",
            "source": "Salary",
            "description": "Monthly Salary",
            "date": f"{year}-{month:02d}-01",
            "paymentMethod": "Net Banking",
            "createdAt": datetime.utcnow(),
        }
        db.transactions.insert_one(income_doc)

        if random.random() < 0.3:
            extra_doc = {
                "userId": user_id,
                "type": "income",
                "amount": random.randint(3000, 10000),
                "category": "Income",
                "source": random.choice(["Freelance", "Investment", "Bonus"]),
                "description": random.choice(["Freelance project", "Dividend income", "Performance bonus"]),
                "date": f"{year}-{month:02d}-{random.randint(5, 25):02d}",
                "paymentMethod": "Net Banking",
                "createdAt": datetime.utcnow(),
            }
            db.transactions.insert_one(extra_doc)

        num_expenses = random.randint(12, 22)
        for _ in range(num_expenses):
            cat = random.choices(cats, weights=weights, k=1)[0]
            desc = random.choice(CATEGORY_ITEMS[cat])
            low, high = CATEGORY_AMOUNTS[cat]
            amount = round(random.uniform(low, high), 0)
            day = random.randint(1, 28)
            tx_doc = {
                "userId": user_id,
                "type": "expense",
                "amount": amount,
                "category": cat,
                "source": "",
                "description": desc,
                "date": f"{year}-{month:02d}-{day:02d}",
                "paymentMethod": random.choice(PAYMENT_METHODS),
                "createdAt": datetime.utcnow(),
            }
            db.transactions.insert_one(tx_doc)

    print("Creating budgets...")
    current_month = f"{now.year}-{now.month:02d}"
    budget_data = [
        ("Food", 10000),
        ("Transport", 5000),
        ("Shopping", 6000),
        ("Bills", 7000),
        ("Entertainment", 4000),
        ("Healthcare", 3000),
        ("Rent", 10000),
        ("Education", 3000),
    ]
    for cat, amount in budget_data:
        db.budgets.insert_one({
            "userId": user_id,
            "month": current_month,
            "category": cat,
            "budgetAmount": amount,
            "createdAt": datetime.utcnow(),
        })

    print("Creating savings goals...")
    goals = [
        {
            "userId": user_id,
            "goalName": "Emergency Fund",
            "targetAmount": 150000,
            "currentAmount": 85000,
            "targetDate": "2026-12-31",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        },
        {
            "userId": user_id,
            "goalName": "New Laptop",
            "targetAmount": 80000,
            "currentAmount": 35000,
            "targetDate": "2026-09-30",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        },
        {
            "userId": user_id,
            "goalName": "Vacation Fund",
            "targetAmount": 50000,
            "currentAmount": 12000,
            "targetDate": "2027-03-01",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        },
        {
            "userId": user_id,
            "goalName": "Car Down Payment",
            "targetAmount": 300000,
            "currentAmount": 45000,
            "targetDate": "2027-06-30",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        },
    ]
    for goal in goals:
        db.savings_goals.insert_one(goal)

    print("Creating alerts...")
    alerts = [
        {"userId": user_id, "type": "info", "title": "Welcome to FinWise AI!", "message": "Your demo account is ready. Explore all features!", "read": False, "createdAt": datetime.utcnow()},
        {"userId": user_id, "type": "warning", "title": "Food Budget Warning", "message": "Your Food budget is 75% used this month.", "read": False, "createdAt": datetime.utcnow()},
        {"userId": user_id, "type": "positive", "title": "Great Savings!", "message": "You saved 18% of your income last month. Keep it up!", "read": True, "createdAt": datetime.utcnow() - timedelta(days=5)},
        {"userId": user_id, "type": "info", "title": "Goal Progress", "message": "You reached 57% of your Emergency Fund goal!", "read": False, "createdAt": datetime.utcnow() - timedelta(days=2)},
        {"userId": user_id, "type": "critical", "title": "Shopping Budget Alert", "message": "Your Shopping spending increased by 22% compared to last month.", "read": False, "createdAt": datetime.utcnow() - timedelta(days=1)},
    ]
    for alert in alerts:
        db.alerts.insert_one(alert)

    print("\n" + "=" * 50)
    print("DEMO ACCOUNT CREATED SUCCESSFULLY!")
    print("=" * 50)
    print(f"Email:    demo@finwise.ai")
    print(f"Password: Demo@123")
    print(f"User ID:  {user_id}")
    print("=" * 50)
    print("\nDemo data includes:")
    print("  - 6 months of income records")
    print("  - 80+ expense records across all categories")
    print("  - 8 budget categories")
    print("  - 4 savings goals with progress")
    print("  - 5 alerts")
    print("\nStart the app and log in to see the data!")


if __name__ == "__main__":
    seed()
