import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/finwise_ai")
    JWT_SECRET = os.getenv("JWT_SECRET", "finwise-secret-key-2026")
    JWT_EXPIRATION_HOURS = 72
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
