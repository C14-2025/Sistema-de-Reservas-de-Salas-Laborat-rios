from pymongo import MongoClient
import os

MONGO_URI = os.getenv(
    "MONGO_URI",

    "mongodb+srv://teste_user:Lucas123*@cluster0.sgaa8y8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
DB_NAME = os.getenv("db", "users")

try:
    client = MongoClient(MONGO_URI)
    # teste de conexão
    client.admin.command("ping")
    print("Conexão com MongoDB Atlas bem-sucedida!")
except Exception as e:
    print("Erro ao conectar no MongoDB:", e)

db = client[DB_NAME]
users_coll = db["users"]
