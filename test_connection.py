from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv("data.env")
uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri, tlsCAFile=certifi.where())
    print("✅ Connection successful! Databases:")
    print(client.list_database_names())
except Exception as e:
    print("❌ Connection failed:", e)
