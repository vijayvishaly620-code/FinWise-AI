from flask import Blueprint, request, jsonify
from routes.auth import token_required
from database import get_db
from models.transaction_model import TransactionModel
from models.budget_model import BudgetModel
from models.savings_model import SavingsModel
from utils.calculations import calculate_financial_health_score

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
@token_required
def get_summary(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    savings_model = SavingsModel(db)
    month = request.args.get("month")
    year = request.args.get("year")
    summary = tx_model.get_summary(current_user["_id"], month, year)
    total_savings = savings_model.get_total_savings(current_user["_id"])
    health_score = calculate_financial_health_score(db, current_user["_id"])
    category_summary = tx_model.get_category_summary(current_user["_id"], month, year)
    highest_category = category_summary[0] if category_summary else None
    savings_rate = round((summary["balance"] / summary["income"] * 100), 1) if summary["income"] > 0 else 0
    expense_ratio = round((summary["expense"] / summary["income"] * 100), 1) if summary["income"] > 0 else 0
    return jsonify({
        "totalIncome": summary["income"],
        "totalExpenses": summary["expense"],
        "balance": summary["balance"],
        "totalSavings": total_savings,
        "savingsRate": savings_rate,
        "expenseRatio": expense_ratio,
        "healthScore": health_score,
        "highestCategory": highest_category,
        "categorySummary": category_summary,
        "incomeCount": summary["income_count"],
        "expenseCount": summary["expense_count"],
    }), 200


@dashboard_bp.route("/analytics", methods=["GET"])
@token_required
def get_analytics(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    monthly_trend = tx_model.get_monthly_trend(current_user["_id"])
    monthly_data = {}
    for entry in monthly_trend:
        month = entry["_id"]["month"]
        tx_type = entry["_id"]["type"]
        if month not in monthly_data:
            monthly_data[month] = {"month": month, "income": 0, "expense": 0}
        monthly_data[month][tx_type] = entry["total"]
    trend = sorted(monthly_data.values(), key=lambda x: x["month"])
    category_summary = tx_model.get_category_summary(current_user["_id"])
    category_data = [{"name": c["_id"], "value": c["total"], "count": c["count"]} for c in category_summary]
    return jsonify({
        "monthlyTrend": trend,
        "categoryDistribution": category_data,
    }), 200
