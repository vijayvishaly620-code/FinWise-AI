from pymongo import MongoClient
from config import Config

client = None
db = None


def get_db():
    global client, db
    if client is None:
        client = MongoClient(Config.MONGO_URI)
        db = client.get_database()
    return db
