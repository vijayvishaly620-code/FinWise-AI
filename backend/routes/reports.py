import csv
import io
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, Response
from routes.auth import token_required
from database import get_db
from models.transaction_model import TransactionModel
from models.budget_model import BudgetModel
from models.savings_model import SavingsModel
from utils.calculations import calculate_financial_health_score

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/monthly", methods=["GET"])
@token_required
def monthly_report(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    budget_model = BudgetModel(db)
    now = datetime.now()
    month = request.args.get("month", str(now.month))
    year = request.args.get("year", str(now.year))
    summary = tx_model.get_summary(current_user["_id"], month, year)
    categories = tx_model.get_category_summary(current_user["_id"], month, year)
    budgets = budget_model.get_all(current_user["_id"], f"{year}-{int(month):02d}")
    for b in budgets:
        spent = sum(c["total"] for c in categories if c["_id"] == b["category"])
        b["spent"] = spent
        b["remaining"] = b["budgetAmount"] - spent
        b["percentage"] = round((spent / b["budgetAmount"]) * 100, 1) if b["budgetAmount"] > 0 else 0
    health = calculate_financial_health_score(db, current_user["_id"])
    top_categories = [{"name": c["_id"], "amount": c["total"], "count": c["count"]} for c in categories[:5]]
    return jsonify({
        "period": {"month": int(month), "year": int(year)},
        "summary": summary,
        "categories": top_categories,
        "budgetPerformance": budgets,
        "healthScore": health,
    }), 200


@reports_bp.route("/yearly", methods=["GET"])
@token_required
def yearly_report(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    now = datetime.now()
    year = request.args.get("year", str(now.year))
    monthly_data = []
    total_income = 0
    total_expense = 0
    for m in range(1, 13):
        summary = tx_model.get_summary(current_user["_id"], str(m), year)
        monthly_data.append({
            "month": m,
            "income": summary["income"],
            "expense": summary["expense"],
            "savings": summary["balance"],
        })
        total_income += summary["income"]
        total_expense += summary["expense"]
    return jsonify({
        "year": int(year),
        "totalIncome": total_income,
        "totalExpenses": total_expense,
        "totalSavings": total_income - total_expense,
        "monthlyBreakdown": monthly_data,
    }), 200


@reports_bp.route("/download", methods=["GET"])
@token_required
def download_report(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    start_date = request.args.get("start_date", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
    end_date = request.args.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    transactions = tx_model.get_by_month_range(current_user["_id"], start_date, end_date)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Type", "Category", "Amount", "Description", "Payment Method"])
    for t in transactions:
        writer.writerow([
            t.get("date", ""),
            t.get("type", ""),
            t.get("category", ""),
            t.get("amount", 0),
            t.get("description", ""),
            t.get("paymentMethod", ""),
        ])
    csv_content = output.getvalue()
    output.close()
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=finwise_report_{start_date}_to_{end_date}.csv"}
    )
