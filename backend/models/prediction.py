from datetime import datetime
from bson import ObjectId
from .db import db

predictions = db["predictions"]
predictions.create_index([("user_id", 1), ("created_at", -1)])


def _serialize(doc):
    doc["_id"] = str(doc["_id"])
    if isinstance(doc.get("created_at"), datetime):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


class PredictionModel:
    @staticmethod
    def create(user_id, kind, input, result):
        doc = {
            "user_id": ObjectId(user_id),
            "kind": kind,
            "input": input,
            "result": result,
            "created_at": datetime.utcnow(),
        }
        predictions.insert_one(doc)

    @staticmethod
    def list_for_user(user_id, limit=50):
        cur = (
            predictions.find({"user_id": ObjectId(user_id)})
            .sort("created_at", -1)
            .limit(limit)
        )
        items = []
        for d in cur:
            d["user_id"] = str(d["user_id"])
            items.append(_serialize(d))
        return items

    @staticmethod
    def summary_for_user(user_id):
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$group": {
                "_id": "$kind",
                "count": {"$sum": 1},
                "avg_probability": {"$avg": "$result.probability"},
            }},
        ]
        return {row["_id"]: {"count": row["count"], "avg_probability": row["avg_probability"]}
                for row in predictions.aggregate(pipeline)}
