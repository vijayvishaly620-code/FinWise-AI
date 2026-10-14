from flask import Blueprint, request, jsonify
from routes.auth import token_required
from database import get_db
from models.budget_model import BudgetModel
from models.transaction_model import TransactionModel

budgets_bp = Blueprint("budgets", __name__)


@budgets_bp.route("", methods=["GET"])
@token_required
def get_budgets(current_user):
    db = get_db()
    budget_model = BudgetModel(db)
    tx_model = TransactionModel(db)
    month = request.args.get("month")
    budgets = budget_model.get_all(current_user["_id"], month)
    for b in budgets:
        cat_summary = tx_model.get_category_summary(current_user["_id"])
        spent = 0
        for c in cat_summary:
            if c["_id"] == b["category"]:
                spent = c["total"]
                break
        b["spent"] = spent
        b["remaining"] = b["budgetAmount"] - spent
        b["percentage"] = round((spent / b["budgetAmount"]) * 100, 1) if b["budgetAmount"] > 0 else 0
        if b["percentage"] >= 100:
            b["status"] = "exceeded"
        elif b["percentage"] >= 90:
            b["status"] = "critical"
        elif b["percentage"] >= 70:
            b["status"] = "warning"
        else:
            b["status"] = "ok"
    return jsonify({"budgets": budgets}), 200


@budgets_bp.route("", methods=["POST"])
@token_required
def create_budget(current_user):
    data = request.get_json()
    if not data or not data.get("category") or not data.get("budgetAmount"):
        return jsonify({"error": "Category and budget amount required"}), 400
    db = get_db()
    budget_model = BudgetModel(db)
    budget = budget_model.create(current_user["_id"], data)
    return jsonify({"budget": budget, "message": "Budget created"}), 201


@budgets_bp.route("/<budget_id>", methods=["PUT"])
@token_required
def update_budget(current_user, budget_id):
    data = request.get_json()
    db = get_db()
    budget_model = BudgetModel(db)
    existing = budget_model.get_by_id(budget_id, current_user["_id"])
    if not existing:
        return jsonify({"error": "Budget not found"}), 404
    updated = budget_model.update(budget_id, current_user["_id"], data)
    return jsonify({"budget": updated, "message": "Budget updated"}), 200


@budgets_bp.route("/<budget_id>", methods=["DELETE"])
@token_required
def delete_budget(current_user, budget_id):
    db = get_db()
    budget_model = BudgetModel(db)
    existing = budget_model.get_by_id(budget_id, current_user["_id"])
    if not existing:
        return jsonify({"error": "Budget not found"}), 404
    budget_model.delete(budget_id, current_user["_id"])
    return jsonify({"message": "Budget deleted"}), 200
