import os
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment or use default
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Synchronous client for initialization tasks
sync_client = MongoClient(MONGO_URI)
db = sync_client["voodo_db"]

# Async client for FastAPI operations
async_client = AsyncIOMotorClient(MONGO_URI)
async_db = async_client["voodo_db"]

# Create collections if they don't exist
if "users" not in db.list_collection_names():
    db.create_collection("users")

if "hangouts" not in db.list_collection_names():
    db.create_collection("hangouts")

if "chat_logs" not in db.list_collection_names():
    db.create_collection("chat_logs")

# Export collections for use in other modules
users_collection = async_db.users
hangouts_collection = async_db.hangouts
chat_logs_collection = async_db.chat_logs

def get_db():
    return async_db
