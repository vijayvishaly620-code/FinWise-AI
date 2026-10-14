import os
from flask import Blueprint, request, jsonify
from routes.auth import token_required
from database import get_db
from models.transaction_model import TransactionModel
from models.budget_model import BudgetModel
from models.savings_model import SavingsModel
from services.advisor_service import RuleBasedAdvisor
from services.ml_service import MLPredictor

advisor_bp = Blueprint("advisor", __name__)


@advisor_bp.route("/analyze", methods=["POST"])
@token_required
def analyze(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    budget_model = BudgetModel(db)
    savings_model = SavingsModel(db)
    summary = tx_model.get_summary(current_user["_id"])
    categories = tx_model.get_category_summary(current_user["_id"])
    budgets = budget_model.get_all(current_user["_id"])
    goals = savings_model.get_all(current_user["_id"])
    user_data = {
        "monthlyIncome": current_user.get("monthlyIncome", summary["income"]),
        "totalIncome": summary["income"],
        "totalExpenses": summary["expense"],
        "balance": summary["balance"],
        "savingsRate": round((summary["balance"] / summary["income"] * 100), 1) if summary["income"] > 0 else 0,
        "categories": {c["_id"]: c["total"] for c in categories},
        "budgets": budgets,
        "savingsGoals": goals,
    }
    advisor = RuleBasedAdvisor()
    advice = advisor.generate_advice(user_data)
    ml_result = None
    try:
        predictor = MLPredictor()
        ml_result = predictor.predict_health(user_data)
    except Exception:
        ml_result = {"health": "Unknown", "confidence": 0, "message": "ML model not available. Train the model first."}
    return jsonify({
        "advice": advice,
        "mlPrediction": ml_result,
        "userData": user_data,
    }), 200


@advisor_bp.route("/chat", methods=["POST"])
@token_required
def chat(current_user):
    data = request.get_json()
    message = data.get("message", "").lower()
    db = get_db()
    tx_model = TransactionModel(db)
    budget_model = BudgetModel(db)
    savings_model = SavingsModel(db)
    summary = tx_model.get_summary(current_user["_id"])
    categories = tx_model.get_category_summary(current_user["_id"])
    budgets = budget_model.get_all(current_user["_id"])
    goals = savings_model.get_all(current_user["_id"])
    advisor = RuleBasedAdvisor()
    user_data = {
        "monthlyIncome": current_user.get("monthlyIncome", summary["income"]),
        "totalIncome": summary["income"],
        "totalExpenses": summary["expense"],
        "balance": summary["balance"],
        "savingsRate": round((summary["balance"] / summary["income"] * 100), 1) if summary["income"] > 0 else 0,
        "categories": {c["_id"]: c["total"] for c in categories},
        "budgets": budgets,
        "savingsGoals": goals,
    }
    response = advisor.chat_response(message, user_data)
    return jsonify({"response": response}), 200


@advisor_bp.route("/predict-expenses", methods=["POST"])
@token_required
def predict_expenses(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    summary = tx_model.get_summary(current_user["_id"])
    categories = tx_model.get_category_summary(current_user["_id"])
    cat_map = {c["_id"]: c["total"] for c in categories}
    history = tx_model.get_monthly_trend(current_user["_id"], months=6)
    monthly_expenses = []
    for entry in history:
        if entry["_id"]["type"] == "expense":
            monthly_expenses.append(entry["total"])
    ml_prediction = None
    try:
        predictor = MLPredictor()
        user_data = {
            "monthlyIncome": current_user.get("monthlyIncome", summary["income"]),
            "totalIncome": summary["income"],
            "totalExpenses": summary["expense"],
            "categories": cat_map,
        }
        ml_result = predictor.predict_expenses(user_data)
        ml_prediction = ml_result.get("predicted", 0)
    except Exception:
        ml_prediction = None
    if len(monthly_expenses) < 2:
        avg = monthly_expenses[0] if monthly_expenses else 0
        rule_prediction = avg
    else:
        recent = monthly_expenses[-1]
        avg_3 = sum(monthly_expenses[-3:]) / min(3, len(monthly_expenses))
        rule_prediction = round(recent * 0.6 + avg_3 * 0.4, 2)
    final_prediction = ml_prediction if ml_prediction else rule_prediction
    return jsonify({
        "predictedExpense": final_prediction,
        "mlPrediction": ml_prediction,
        "rulePrediction": rule_prediction,
        "historicalExpenses": monthly_expenses,
        "disclaimer": "This prediction is an estimate based on historical spending patterns."
    }), 200


@advisor_bp.route("/financial-health", methods=["GET"])
@token_required
def financial_health(current_user):
    db = get_db()
    from utils.calculations import calculate_financial_health_score
    score = calculate_financial_health_score(db, current_user["_id"])
    return jsonify({"score": score}), 200
