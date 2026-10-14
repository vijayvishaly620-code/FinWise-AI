from datetime import datetime
from bson import ObjectId


class BudgetModel:
    def __init__(self, db):
        self.collection = db.budgets

    def create(self, user_id, data):
        budget = {
            "userId": user_id,
            "month": data["month"],
            "category": data["category"],
            "budgetAmount": float(data["budgetAmount"]),
            "createdAt": datetime.utcnow(),
        }
        result = self.collection.insert_one(budget)
        budget["_id"] = str(result.inserted_id)
        return budget

    def get_all(self, user_id, month=None):
        query = {"userId": user_id}
        if month:
            query["month"] = month
        budgets = list(self.collection.find(query))
        for b in budgets:
            b["_id"] = str(b["_id"])
        return budgets

    def get_by_id(self, budget_id, user_id):
        b = self.collection.find_one(
            {"_id": ObjectId(budget_id), "userId": user_id}
        )
        if b:
            b["_id"] = str(b["_id"])
        return b

    def update(self, budget_id, user_id, data):
        update_fields = {}
        if "budgetAmount" in data:
            update_fields["budgetAmount"] = float(data["budgetAmount"])
        if "month" in data:
            update_fields["month"] = data["month"]
        if "category" in data:
            update_fields["category"] = data["category"]
        self.collection.update_one(
            {"_id": ObjectId(budget_id), "userId": user_id},
            {"$set": update_fields}
        )
        return self.get_by_id(budget_id, user_id)

    def delete(self, budget_id, user_id):
        result = self.collection.delete_one(
            {"_id": ObjectId(budget_id), "userId": user_id}
        )
        return result.deleted_count > 0

    def get_by_month_category(self, user_id, month, category):
        b = self.collection.find_one({
            "userId": user_id,
            "month": month,
            "category": category
        })
        if b:
            b["_id"] = str(b["_id"])
        return b
