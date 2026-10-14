from datetime import datetime
from bson import ObjectId


class TransactionModel:
    def __init__(self, db):
        self.collection = db.transactions

    def create(self, user_id, data):
        transaction = {
            "userId": user_id,
            "type": data["type"],
            "amount": float(data["amount"]),
            "category": data.get("category", "Other"),
            "source": data.get("source", ""),
            "description": data.get("description", ""),
            "date": data.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
            "paymentMethod": data.get("paymentMethod", "Other"),
            "createdAt": datetime.utcnow(),
        }
        result = self.collection.insert_one(transaction)
        transaction["_id"] = str(result.inserted_id)
        return transaction

    def get_all(self, user_id, filters=None):
        query = {"userId": user_id}
        if filters:
            if filters.get("type"):
                query["type"] = filters["type"]
            if filters.get("category"):
                query["category"] = filters["category"]
            if filters.get("start_date") and filters.get("end_date"):
                query["date"] = {
                    "$gte": filters["start_date"],
                    "$lte": filters["end_date"]
                }
            if filters.get("search"):
                query["$or"] = [
                    {"description": {"$regex": filters["search"], "$options": "i"}},
                    {"category": {"$regex": filters["search"], "$options": "i"}},
                    {"source": {"$regex": filters["search"], "$options": "i"}},
                ]
        sort_field = filters.get("sort_by", "date") if filters else "date"
        sort_dir = -1 if filters and filters.get("sort_dir") == "desc" else -1
        transactions = list(self.collection.find(query).sort(sort_field, sort_dir))
        for t in transactions:
            t["_id"] = str(t["_id"])
        return transactions

    def get_by_id(self, transaction_id, user_id):
        t = self.collection.find_one(
            {"_id": ObjectId(transaction_id), "userId": user_id}
        )
        if t:
            t["_id"] = str(t["_id"])
        return t

    def update(self, transaction_id, user_id, data):
        update_fields = {}
        allowed = ["type", "amount", "category", "source", "description", "date", "paymentMethod"]
        for field in allowed:
            if field in data:
                update_fields[field] = data[field]
        if "amount" in update_fields:
            update_fields["amount"] = float(update_fields["amount"])
        self.collection.update_one(
            {"_id": ObjectId(transaction_id), "userId": user_id},
            {"$set": update_fields}
        )
        return self.get_by_id(transaction_id, user_id)

    def delete(self, transaction_id, user_id):
        result = self.collection.delete_one(
            {"_id": ObjectId(transaction_id), "userId": user_id}
        )
        return result.deleted_count > 0

    def get_summary(self, user_id, month=None, year=None):
        pipeline = [{"$match": {"userId": user_id}}]
        if month and year:
            date_str = f"{year}-{int(month):02d}"
            pipeline.append({"$match": {"date": {"$regex": f"^{date_str}"}}})
        pipeline.extend([
            {"$group": {
                "_id": "$type",
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }}
        ])
        results = list(self.collection.aggregate(pipeline))
        summary = {"income": 0, "expense": 0, "income_count": 0, "expense_count": 0}
        for r in results:
            if r["_id"] == "income":
                summary["income"] = r["total"]
                summary["income_count"] = r["count"]
            elif r["_id"] == "expense":
                summary["expense"] = r["total"]
                summary["expense_count"] = r["count"]
        summary["balance"] = summary["income"] - summary["expense"]
        return summary

    def get_category_summary(self, user_id, month=None, year=None):
        match = {"userId": user_id, "type": "expense"}
        if month and year:
            date_str = f"{year}-{int(month):02d}"
            match["date"] = {"$regex": f"^{date_str}"}
        pipeline = [
            {"$match": match},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
            {"$sort": {"total": -1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_monthly_trend(self, user_id, months=6):
        pipeline = [
            {"$match": {"userId": user_id}},
            {"$addFields": {"month": {"$substr": ["$date", 0, 7]}}},
            {"$group": {
                "_id": {"month": "$month", "type": "$type"},
                "total": {"$sum": "$amount"}
            }},
            {"$sort": {"_id.month": 1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_by_month_range(self, user_id, start_date, end_date):
        query = {
            "userId": user_id,
            "date": {"$gte": start_date, "$lte": end_date}
        }
        transactions = list(self.collection.find(query).sort("date", -1))
        for t in transactions:
            t["_id"] = str(t["_id"])
        return transactions
