from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient
import os

# Caminho até o .env que está uma pasta acima
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DEBUG - .env carregado de:", env_path)
print("DEBUG - MONGO_URI:", os.getenv("MONGO_URI"))
print("DEBUG - DB_NAME:", os.getenv("DB_NAME"))

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "db")

client: None
db: None
users_coll: None
labs_coll: None

async def connect_to_mongo():
    global client, db, users_coll, labs_coll
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command("ping")
        db = client[DB_NAME]

        users_coll = db["users"]

        print("✅ Conectado ao MongoDB com sucesso!")

        return True
    except Exception as e:
        print("❌ Erro ao conectar no MongoDB:", e)
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

def get_labs_collection():
    global labs_coll
    if labs_coll is None:
        raise Exception("❌ Conexão com banco de dados não encontrado")
    return labs_coll

