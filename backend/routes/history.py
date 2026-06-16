from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.prediction import PredictionModel

history_bp = Blueprint("history", __name__)


@history_bp.get("/history")
@jwt_required()
def history():
    uid = get_jwt_identity()
    limit = int(request.args.get("limit", 50))
    items = PredictionModel.list_for_user(uid, limit=limit)
    return jsonify(items=items, count=len(items))


@history_bp.get("/reports")
@jwt_required()
def reports():
    uid = get_jwt_identity()
    summary = PredictionModel.summary_for_user(uid)
    return jsonify(summary)
