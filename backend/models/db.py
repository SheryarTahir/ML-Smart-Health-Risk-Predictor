from pymongo import MongoClient
from config.config import Config

_client = MongoClient(Config.MONGO_URI)
db = _client[Config.MONGO_DB]
