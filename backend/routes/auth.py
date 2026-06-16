from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models.user import UserModel
from utils.validators import validate_register, validate_login
from utils.hashing import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    err = validate_register(data)
    if err:
        return jsonify(error=err), 400
    if UserModel.find_by_email(data["email"]):
        return jsonify(error="Email already registered"), 409
    user_id = UserModel.create(
        name=data["name"],
        email=data["email"].lower(),
        password_hash=hash_password(data["password"]),
    )
    token = create_access_token(identity=str(user_id))
    return jsonify(message="Registered", token=token, user_id=str(user_id)), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    err = validate_login(data)
    if err:
        return jsonify(error=err), 400
    user = UserModel.find_by_email(data["email"].lower())
    if not user or not verify_password(data["password"], user["password_hash"]):
        return jsonify(error="Invalid credentials"), 401
    token = create_access_token(identity=str(user["_id"]))
    return jsonify(
        message="Logged in",
        token=token,
        user={"id": str(user["_id"]), "name": user["name"], "email": user["email"]},
    )


@auth_bp.post("/logout")
@jwt_required()
def logout():
    # With stateless JWT, logout is a client-side token discard.
    # For server-side revocation, integrate a denylist (Redis).
    return jsonify(message="Logged out")


@auth_bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = UserModel.find_by_id(uid)
    if not user:
        return jsonify(error="Not found"), 404
    return jsonify(id=str(user["_id"]), name=user["name"], email=user["email"])
