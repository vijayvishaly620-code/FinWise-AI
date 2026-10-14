from datetime import datetime
from bson import ObjectId


class AlertModel:
    def __init__(self, db):
        self.collection = db.alerts

    def create(self, user_id, data):
        alert = {
            "userId": user_id,
            "type": data.get("type", "info"),
            "title": data["title"],
            "message": data["message"],
            "read": False,
            "createdAt": datetime.utcnow(),
        }
        result = self.collection.insert_one(alert)
        alert["_id"] = str(result.inserted_id)
        return alert

    def get_all(self, user_id, unread_only=False):
        query = {"userId": user_id}
        if unread_only:
            query["read"] = False
        alerts = list(self.collection.find(query).sort("createdAt", -1))
        for a in alerts:
            a["_id"] = str(a["_id"])
        return alerts

    def mark_read(self, alert_id, user_id):
        self.collection.update_one(
            {"_id": ObjectId(alert_id), "userId": user_id},
            {"$set": {"read": True}}
        )
        return True

    def count_unread(self, user_id):
        return self.collection.count_documents({"userId": user_id, "read": False})

    def delete_old(self, user_id, days=90):
        cutoff = datetime.utcnow()
        cutoff = cutoff.replace(day=cutoff.day - days) if cutoff.day > days else cutoff
        self.collection.delete_many({
            "userId": user_id,
            "createdAt": {"$lt": cutoff}
        })
