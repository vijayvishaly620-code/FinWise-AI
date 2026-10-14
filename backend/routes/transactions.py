from flask import Blueprint, request, jsonify
from routes.auth import token_required
from database import get_db
from models.transaction_model import TransactionModel
from utils.calculations import generate_alerts_for_transactions

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("", methods=["GET"])
@token_required
def get_transactions(current_user):
    db = get_db()
    tx_model = TransactionModel(db)
    filters = {
        "type": request.args.get("type"),
        "category": request.args.get("category"),
        "start_date": request.args.get("start_date"),
        "end_date": request.args.get("end_date"),
        "search": request.args.get("search"),
        "sort_by": request.args.get("sort_by", "date"),
        "sort_dir": request.args.get("sort_dir", "desc"),
    }
    filters = {k: v for k, v in filters.items() if v}
    transactions = tx_model.get_all(current_user["_id"], filters if filters else None)
    return jsonify({"transactions": transactions, "count": len(transactions)}), 200


@transactions_bp.route("", methods=["POST"])
@token_required
def create_transaction(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not data.get("amount") or float(data["amount"]) <= 0:
        return jsonify({"error": "Valid amount is required"}), 400
    if not data.get("type") or data["type"] not in ["income", "expense"]:
        return jsonify({"error": "Type must be income or expense"}), 400
    db = get_db()
    tx_model = TransactionModel(db)
    transaction = tx_model.create(current_user["_id"], data)
    generate_alerts_for_transactions(db, current_user["_id"])
    return jsonify({"transaction": transaction, "message": "Transaction created"}), 201


@transactions_bp.route("/<tx_id>", methods=["PUT"])
@token_required
def update_transaction(current_user, tx_id):
    data = request.get_json()
    db = get_db()
    tx_model = TransactionModel(db)
    existing = tx_model.get_by_id(tx_id, current_user["_id"])
    if not existing:
        return jsonify({"error": "Transaction not found"}), 404
    updated = tx_model.update(tx_id, current_user["_id"], data)
    return jsonify({"transaction": updated, "message": "Transaction updated"}), 200


@transactions_bp.route("/<tx_id>", methods=["DELETE"])
@token_required
def delete_transaction(current_user, tx_id):
    db = get_db()
    tx_model = TransactionModel(db)
    existing = tx_model.get_by_id(tx_id, current_user["_id"])
    if not existing:
        return jsonify({"error": "Transaction not found"}), 404
    tx_model.delete(tx_id, current_user["_id"])
    return jsonify({"message": "Transaction deleted"}), 200
