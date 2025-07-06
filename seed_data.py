import os
import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["voodo_db"]

# Mock data matching the frontend
mock_posts = [
  {
    "username": "night_owl",
    "imageUrl": "https://images.unsplash.com/photo-1485470733090-0aae1788d5af?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1391&q=80",
    "description": "Late night vibes. Anyone up for a chat?",
    "likes": 234,
    "comments": 56,
    "tags": ["night", "vibes", "chat"],
    "created_at": datetime.now()
  },
  {
    "username": "aesthetic_dreams",
    "imageUrl": "https://images.unsplash.com/photo-1620503374956-c942862f0372?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    "description": "Found this perfect spot for stargazing. The sky was unreal.",
    "likes": 512,
    "comments": 89,
    "tags": ["sky", "stars", "night"],
    "created_at": datetime.now()
  },
  {
    "username": "digital_wanderer",
    "imageUrl": "https://images.unsplash.com/photo-1638803040283-7a5ffd48dad5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1374&q=80",
    "description": "Cyberpunk dreams. Feeling the neon tonight.",
    "likes": 789,
    "comments": 104,
    "tags": ["cyberpunk", "neon", "aesthetic"],
    "created_at": datetime.now()
  }
]

async def seed_database():
    """Seed the database with initial data"""
    # Clear existing hangouts collection
    await db.hangouts.delete_many({})
    
    # Insert mock posts
    result = await db.hangouts.insert_many(mock_posts)
    
    print(f"Inserted {len(result.inserted_ids)} hangout posts")

if __name__ == "__main__":
    asyncio.run(seed_database())
