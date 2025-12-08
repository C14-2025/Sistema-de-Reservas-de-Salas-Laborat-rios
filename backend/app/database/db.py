from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient
import os

import mongomock 

# Caminho até o .env que está uma pasta acima
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DEBUG - .env carregado de:", env_path)
print("DEBUG - MONGO_URI:", os.getenv("MONGO_URI"))
print("DEBUG - DB_NAME:", os.getenv("DB_NAME"))

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "db")


TESTING = os.getenv("TESTING") == "1"

client = None
db = None
users_coll = None
labs_coll = None
reservations_coll = None


def _init_db_sync():
    
    global client, db, users_coll, labs_coll, reservations_coll

    if db is not None:
        return True

    print("DEBUG - _init_db_sync chamado")
    print("DEBUG - TESTING:", TESTING)
    print("DEBUG - MONGO_URI:", MONGO_URI)
    print("DEBUG - DB_NAME:", DB_NAME)

    try:
        if TESTING:
            client = mongomock.MongoClient()
            db = client["test_db"]
            print("✅ Usando mongomock (banco em memória) porque TESTING=1")
        else:
            if not MONGO_URI:
                raise Exception("MONGO_URI não definido no ambiente (.env)")

            client = MongoClient(MONGO_URI)
            client.admin.command("ping")
            db = client[DB_NAME]
            print("✅ Conectado ao MongoDB real com sucesso!")

        global users_coll, labs_coll, reservations_coll
        users_coll = db["users"]
        labs_coll = db["labs"]
        reservations_coll = db["reservations"]

        print("DEBUG - Databases in cluster (mock ou real):", client.list_database_names())
        print("DEBUG - Collections inside DB_NAME:", db.list_collection_names())
        print("DEBUG - Labs collection reference:", labs_coll)

        return True

    except Exception as e:
        print("❌ Erro ao conectar no MongoDB:", e)
        client = None
        db = None
        users_coll = None
        labs_coll = None
        reservations_coll = None
        return False


async def connect_to_mongo():
    
    ok = _init_db_sync()
    return ok


async def close_connection_to_mongo():
    global client, db, users_coll, labs_coll, reservations_coll
    if client:
        client.close()
        client = None
        db = None
        users_coll = None
        labs_coll = None
        reservations_coll = None
        print("✅ Conexão com MongoDB fechada")
        return True
    return False


def get_database():
    if db is None:
        _init_db_sync()
    if db is None:
        raise Exception("❌ Conexão com banco de dados não encontrado")
    return db


def get_users_collection():
    if users_coll is None:
        _init_db_sync()
    if users_coll is None:
        raise Exception("❌ Users_coll não inicializado")
    return users_coll


def get_labs_collection():
    if labs_coll is None:
        _init_db_sync()
    if labs_coll is None:
        raise Exception("❌ Labs_coll não inicializado")
    return labs_coll


def get_reservations_collection():
    if reservations_coll is None:
        _init_db_sync()
    if reservations_coll is None:
        raise Exception("❌ Reservations_coll não inicializado")
    return reservations_coll
