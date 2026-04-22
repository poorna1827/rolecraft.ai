from pymongo import MongoClient
from resume_writer.core.config import settings

class Database:
    client: MongoClient = None

db = Database()

def get_database():
    return db.client[settings.MONGODB_DB_NAME]

def connect_to_mongo():
    try:
        db.client = MongoClient(settings.MONGODB_URI)
        # Verify connection
        db.client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

def close_mongo_connection():
    if db.client is not None:
        db.client.close()
        print("Closed MongoDB connection")
