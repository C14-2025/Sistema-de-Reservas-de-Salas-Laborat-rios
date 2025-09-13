from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "db")

client: None
db: None
users_coll: None


async def connect_to_mongo():
    global client, db, users_coll
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command("ping")
        db = client[DB_NAME]
        users_coll = db["users"]
        return True
    except Exception as e:
        return False


async def close_connection_to_mongo():
    global client
    if client:
        client.close()
        print("✅ Conexão com MongoDB fechada")
        return True
    return False


def get_database():
    global db
    if db is None:
        raise Exception("❌ Conexão com banco de dados não encontrado")
    return db


def get_users_collection():
    global users_coll
    if users_coll is None:
        raise Exception("❌ Conexão com banco de dados não encontrado")
    return users_coll
