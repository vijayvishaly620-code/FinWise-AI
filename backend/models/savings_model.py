from datetime import datetime
from bson import ObjectId


class SavingsModel:
    def __init__(self, db):
        self.collection = db.savings_goals

    def create(self, user_id, data):
        goal = {
            "userId": user_id,
            "goalName": data["goalName"],
            "targetAmount": float(data["targetAmount"]),
            "currentAmount": float(data.get("currentAmount", 0)),
            "targetDate": data.get("targetDate", ""),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
        result = self.collection.insert_one(goal)
        goal["_id"] = str(result.inserted_id)
        return goal

    def get_all(self, user_id):
        goals = list(self.collection.find({"userId": user_id}))
        for g in goals:
            g["_id"] = str(g["_id"])
        return goals

    def get_by_id(self, goal_id, user_id):
        g = self.collection.find_one(
            {"_id": ObjectId(goal_id), "userId": user_id}
        )
        if g:
            g["_id"] = str(g["_id"])
        return g

    def update(self, goal_id, user_id, data):
        update_fields = {"updatedAt": datetime.utcnow()}
        allowed = ["goalName", "targetAmount", "currentAmount", "targetDate"]
        for field in allowed:
            if field in data:
                update_fields[field] = float(data[field]) if field in ["targetAmount", "currentAmount"] else data[field]
        self.collection.update_one(
            {"_id": ObjectId(goal_id), "userId": user_id},
            {"$set": update_fields}
        )
        return self.get_by_id(goal_id, user_id)

    def delete(self, goal_id, user_id):
        result = self.collection.delete_one(
            {"_id": ObjectId(goal_id), "userId": user_id}
        )
        return result.deleted_count > 0

    def get_total_savings(self, user_id):
        pipeline = [
            {"$match": {"userId": user_id}},
            {"$group": {"_id": None, "total": {"$sum": "$currentAmount"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]["total"] if result else 0
