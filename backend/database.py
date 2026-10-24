from pymongo import MongoClient
from config import Config

client = None
db = None


def ensure_indexes(database):
    """Ensure essential indexes exist for query performance and data integrity."""
    try:
        database.users.create_index("email", unique=True)
        database.transactions.create_index([("userId", 1), ("date", -1)])
        database.transactions.create_index([("userId", 1), ("type", 1)])
        database.budgets.create_index([("userId", 1), ("month", 1)])
        database.savings_goals.create_index("userId")
        database.alerts.create_index([("userId", 1), ("createdAt", -1)])
    except Exception as e:
        print(f"Index initialization warning: {e}")


def get_db():
    global client, db
    if client is None:
        client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            maxPoolSize=50
        )
        db = client.get_default_database(default="finwise_ai")
        ensure_indexes(db)
    return db
