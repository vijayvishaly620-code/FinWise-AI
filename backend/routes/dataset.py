from flask import Blueprint, jsonify
from routes.auth import token_required
from services.ml_service import MLPredictor

dataset_bp = Blueprint("dataset", __name__)


@dataset_bp.route("/info", methods=["GET"])
@token_required
def get_dataset_info(current_user):
    predictor = MLPredictor()
    info = predictor.get_dataset_info()
    if not info:
        return jsonify({"error": "Dataset not found"}), 404
    return jsonify(info), 200
