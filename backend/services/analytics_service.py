from models.transaction_model import TransactionModel


class AnalyticsService:
    def __init__(self, db):
        self.tx_model = TransactionModel(db)

    def get_spending_patterns(self, user_id, months=6):
        trend = self.tx_model.get_monthly_trend(user_id, months)
        monthly_data = {}
        for entry in trend:
            month = entry["_id"]["month"]
            tx_type = entry["_id"]["type"]
            if month not in monthly_data:
                monthly_data[month] = {"month": month, "income": 0, "expense": 0}
            monthly_data[month][tx_type] = entry["total"]
        result = sorted(monthly_data.values(), key=lambda x: x["month"])
        for item in result:
            item["savings"] = item["income"] - item["expense"]
            item["savingsRate"] = round((item["savings"] / item["income"] * 100), 1) if item["income"] > 0 else 0
        return result

    def get_category_trends(self, user_id):
        categories = self.tx_model.get_category_summary(user_id)
        total = sum(c["total"] for c in categories) if categories else 0
        result = []
        for c in categories:
            result.append({
                "category": c["_id"],
                "amount": c["total"],
                "percentage": round((c["total"] / total) * 100, 1) if total > 0 else 0,
                "count": c["count"],
            })
        return result

    def detect_anomalies(self, user_id):
        trend = self.get_spending_patterns(user_id, 6)
        if len(trend) < 3:
            return []
        expenses = [t["expense"] for t in trend]
        avg = sum(expenses) / len(expenses)
        std = (sum((e - avg) ** 2 for e in expenses) / len(expenses)) ** 0.5
        anomalies = []
        for t in trend:
            if t["expense"] > avg + 1.5 * std:
                anomalies.append({
                    "month": t["month"],
                    "amount": t["expense"],
                    "average": round(avg, 2),
                    "message": f"Spending in {t['month']} was significantly higher than average."
                })
        return anomalies
