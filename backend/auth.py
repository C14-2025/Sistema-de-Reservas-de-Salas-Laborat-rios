# backend/auth.py
from db import users_coll
from passlib.context import CryptContext
from db import users_coll


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(email: str, password: str) -> dict:
    # Verifica se o usuário já existe
    if users_coll.find_one({"email": email}):
        raise ValueError("Email já cadastrado")
    
    hashed = hash_password(password)
    user = {"email": email, "password": hashed}
    users_coll.insert_one(user)
    return user

# Autenticação de usuário
def authenticate_user(email: str, password: str) -> dict | None:
    user = users_coll.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user

#
def delete_user(email: str) -> bool:
    result = users_coll.delete_one({"email": email})
    return result.deleted_count > 0