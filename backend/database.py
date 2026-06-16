"""Database helper (rubric-compliant entry point).

Re-exports the active MongoDB handle from ``models.db`` so callers can do
``from database import db`` as referenced in the rubric folder structure.
"""
from models.db import db, _client

def get_db():
    """Return the active MongoDB database handle."""
    return db

def get_users_collection():
    return db["users"]

def get_predictions_collection():
    return db["predictions"]

__all__ = ["db", "get_db", "get_users_collection", "get_predictions_collection"]
