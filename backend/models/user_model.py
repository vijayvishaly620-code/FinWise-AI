from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson import ObjectId


class UserModel:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, data):
        user = {
            "fullName": data["fullName"],
            "email": data["email"].lower().strip(),
            "password": generate_password_hash(data["password"]),
            "monthlyIncome": float(data.get("monthlyIncome", 0)),
            "currency": data.get("currency", "INR"),
            "financialGoal": data.get("financialGoal", ""),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
        result = self.collection.insert_one(user)
        user["_id"] = str(result.inserted_id)
        del user["password"]
        return user

    def find_by_email(self, email):
        return self.collection.find_one({"email": email.lower().strip()})

    def find_by_id(self, user_id):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
        return user

    def verify_password(self, stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    def update_user(self, user_id, data):
        update_fields = {}
        allowed = ["fullName", "monthlyIncome", "currency", "financialGoal"]
        for field in allowed:
            if field in data:
                update_fields[field] = data[field]
        update_fields["updatedAt"] = datetime.utcnow()
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields}
        )
        return self.find_by_id(user_id)

    def update_income(self, user_id, income):
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"monthlyIncome": float(income), "updatedAt": datetime.utcnow()}}
        )
