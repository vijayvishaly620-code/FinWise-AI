from flask import Blueprint, request, jsonify
from routes.auth import token_required
from database import get_db
from models.alert_model import AlertModel

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("", methods=["GET"])
@token_required
def get_alerts(current_user):
    db = get_db()
    alert_model = AlertModel(db)
    unread_only = request.args.get("unread", "false").lower() == "true"
    alerts = alert_model.get_all(current_user["_id"], unread_only)
    unread_count = alert_model.count_unread(current_user["_id"])
    return jsonify({"alerts": alerts, "unreadCount": unread_count}), 200


@alerts_bp.route("/<alert_id>/read", methods=["PUT"])
@token_required
def mark_read(current_user, alert_id):
    db = get_db()
    alert_model = AlertModel(db)
    alert_model.mark_read(alert_id, current_user["_id"])
    return jsonify({"message": "Alert marked as read"}), 200
