import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from bson import ObjectId
import json

from flask.json.provider import DefaultJSONProvider
import numpy as np

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (np.integer, np.floating)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super().default(o)

app.json_provider_class = CustomJSONProvider
app.json = CustomJSONProvider(app)

from routes.auth import auth_bp
from routes.transactions import transactions_bp
from routes.budgets import budgets_bp
from routes.savings import savings_bp
from routes.dashboard import dashboard_bp
from routes.advisor import advisor_bp
from routes.reports import reports_bp
from routes.alerts import alerts_bp
from routes.dataset import dataset_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
app.register_blueprint(budgets_bp, url_prefix="/api/budgets")
app.register_blueprint(savings_bp, url_prefix="/api/savings")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
app.register_blueprint(advisor_bp, url_prefix="/api/advisor")
app.register_blueprint(reports_bp, url_prefix="/api/reports")
app.register_blueprint(alerts_bp, url_prefix="/api/alerts")
app.register_blueprint(dataset_bp, url_prefix="/api/dataset")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "FinWise AI Backend is running"})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("Starting FinWise AI Backend...")
    print(f"MongoDB URI: {Config.MONGO_URI}")
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=Config.PORT)
