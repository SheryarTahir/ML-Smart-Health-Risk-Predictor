from datetime import datetime
from bson import ObjectId
from .db import db

users = db["users"]
users.create_index("email", unique=True)


class UserModel:
    @staticmethod
    def create(name, email, password_hash):
        doc = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
        }
        return users.insert_one(doc).inserted_id

    @staticmethod
    def find_by_email(email):
        return users.find_one({"email": email})

    @staticmethod
    def find_by_id(uid):
        try:
            return users.find_one({"_id": ObjectId(uid)})
        except Exception:
            return None
