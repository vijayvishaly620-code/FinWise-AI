from flask import Blueprint, request, jsonify
from routes.auth import token_required
from database import get_db
from models.savings_model import SavingsModel
from datetime import datetime

savings_bp = Blueprint("savings", __name__)


@savings_bp.route("", methods=["GET"])
@token_required
def get_savings(current_user):
    db = get_db()
    savings_model = SavingsModel(db)
    goals = savings_model.get_all(current_user["_id"])
    for g in goals:
        g["progress"] = round((g["currentAmount"] / g["targetAmount"]) * 100, 1) if g["targetAmount"] > 0 else 0
        if g.get("targetDate"):
            try:
                target = datetime.strptime(g["targetDate"], "%Y-%m-%d")
                months_left = max(1, (target.year - datetime.now().year) * 12 + (target.month - datetime.now().month))
                remaining = g["targetAmount"] - g["currentAmount"]
                g["requiredMonthly"] = round(remaining / months_left, 2) if remaining > 0 else 0
                g["monthsRemaining"] = months_left
            except (ValueError, TypeError):
                g["requiredMonthly"] = 0
                g["monthsRemaining"] = 0
        else:
            g["requiredMonthly"] = 0
            g["monthsRemaining"] = 0
    return jsonify({"goals": goals}), 200


@savings_bp.route("", methods=["POST"])
@token_required
def create_savings(current_user):
    data = request.get_json()
    if not data or not data.get("goalName") or not data.get("targetAmount"):
        return jsonify({"error": "Goal name and target amount required"}), 400
    db = get_db()
    savings_model = SavingsModel(db)
    goal = savings_model.create(current_user["_id"], data)
    return jsonify({"goal": goal, "message": "Savings goal created"}), 201


@savings_bp.route("/<goal_id>", methods=["PUT"])
@token_required
def update_savings(current_user, goal_id):
    data = request.get_json()
    db = get_db()
    savings_model = SavingsModel(db)
    existing = savings_model.get_by_id(goal_id, current_user["_id"])
    if not existing:
        return jsonify({"error": "Goal not found"}), 404
    updated = savings_model.update(goal_id, current_user["_id"], data)
    return jsonify({"goal": updated, "message": "Goal updated"}), 200


@savings_bp.route("/<goal_id>", methods=["DELETE"])
@token_required
def delete_savings(current_user, goal_id):
    db = get_db()
    savings_model = SavingsModel(db)
    existing = savings_model.get_by_id(goal_id, current_user["_id"])
    if not existing:
        return jsonify({"error": "Goal not found"}), 404
    savings_model.delete(goal_id, current_user["_id"])
    return jsonify({"message": "Goal deleted"}), 200
