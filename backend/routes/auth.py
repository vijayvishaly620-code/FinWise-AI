import jwt
import datetime
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from database import get_db
from config import Config
from models.user_model import UserModel

auth_bp = Blueprint("auth", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        if not token and "token" in request.args:
            token = request.args.get("token")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            db = get_db()
            user_model = UserModel(db)
            current_user = user_model.find_by_id(data["user_id"])
            if not current_user:
                return jsonify({"error": "User not found"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    required = ["fullName", "email", "password"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
    if data.get("password") != data.get("confirmPassword"):
        return jsonify({"error": "Passwords do not match"}), 400
    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    db = get_db()
    user_model = UserModel(db)
    if user_model.find_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 409
    user = user_model.create_user(data)
    token = jwt.encode(
        {"user_id": user["_id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS)},
        Config.JWT_SECRET,
        algorithm="HS256",
    )
    return jsonify({"message": "Registration successful", "token": token, "user": user}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400
    db = get_db()
    user_model = UserModel(db)
    user = user_model.find_by_email(data["email"])
    if not user or not user_model.verify_password(user["password"], data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    token = jwt.encode(
        {"user_id": str(user["_id"]), "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS)},
        Config.JWT_SECRET,
        algorithm="HS256",
    )
    user_data = {k: v for k, v in user.items() if k != "password"}
    user_data["_id"] = str(user_data["_id"])
    return jsonify({"message": "Login successful", "token": token, "user": user_data}), 200


@auth_bp.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    return jsonify({"user": current_user}), 200


@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    data = request.get_json()
    db = get_db()
    user_model = UserModel(db)
    updated = user_model.update_user(current_user["_id"], data)
    return jsonify({"user": updated}), 200
