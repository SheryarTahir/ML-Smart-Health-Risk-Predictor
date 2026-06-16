from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ml.prediction import predict_heart, predict_diabetes, predict_obesity
from models.prediction import PredictionModel

predict_bp = Blueprint("predict", __name__)


def _save(uid, kind, payload, result):
    PredictionModel.create(user_id=uid, kind=kind, input=payload, result=result)


@predict_bp.post("/heart")
@jwt_required()
def heart():
    data = request.get_json(silent=True) or {}
    try:
        result = predict_heart(data)
    except Exception as e:
        return jsonify(error=str(e)), 400
    _save(get_jwt_identity(), "heart", data, result)
    return jsonify(result)


@predict_bp.post("/diabetes")
@jwt_required()
def diabetes():
    data = request.get_json(silent=True) or {}
    try:
        result = predict_diabetes(data)
    except Exception as e:
        return jsonify(error=str(e)), 400
    _save(get_jwt_identity(), "diabetes", data, result)
    return jsonify(result)


@predict_bp.post("/obesity")
@jwt_required()
def obesity():
    data = request.get_json(silent=True) or {}
    try:
        result = predict_obesity(data)
    except Exception as e:
        return jsonify(error=str(e)), 400
    _save(get_jwt_identity(), "obesity", data, result)
    return jsonify(result)
