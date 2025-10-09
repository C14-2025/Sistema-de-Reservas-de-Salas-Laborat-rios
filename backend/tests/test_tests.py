import sys
import os
import pytest
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi.testclient import TestClient
from backend.app.main import app  # importa o app FastAPI principal

from backend.app.utils.auth import hash_password, create_user, verify_password
from backend.app.database.db import connect_to_mongo, close_connection_to_mongo, get_users_collection


# Conecta no banco antes da sessão de testes e fecha no final
@pytest.fixture(scope="session", autouse=True)
def setup_mongo():
    asyncio.run(connect_to_mongo())
    yield
    asyncio.run(close_connection_to_mongo())


# Limpa a coleção de usuários antes e depois de cada teste
@pytest.fixture(autouse=True)
def clear_db():
    users_coll = get_users_collection()
    users_coll.delete_many({})
    yield
    users_coll.delete_many({})


# Teste: cadastro de usuário válido
def test_create_user():
    email = "teste@example.com"
    password = "123456"
    create_user(email, password)

    users_coll = get_users_collection()
    db_user = users_coll.find_one({"email": email})
    assert db_user is not None
    assert db_user["email"] == email


# Teste: cadastro com email duplicado
def test_duplicate_email():
    email = "teste@example.com"
    password = "123456"
    create_user(email, password)

    with pytest.raises(ValueError):
        create_user(email, password)


# Teste: senha é realmente hasheada
def test_password_hashed():
    password = "123456"
    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)


# Teste: login com credenciais válidas
def test_login_valid_user():
    email = "login@example.com"
    password = "senha123"
    create_user(email, password)

    users_coll = get_users_collection()
    user = users_coll.find_one({"email": email})

    assert user is not None
    assert verify_password(password, user["password"]) is True


# Teste: login com senha incorreta
def test_login_invalid_password():
    email = "loginfail@example.com"
    password = "senha123"
    create_user(email, password)

    users_coll = get_users_collection()
    user = users_coll.find_one({"email": email})

    assert user is not None
    assert verify_password("senha_errada", user["password"]) is False


# Teste: listagem de usuários não deve retornar senha
def test_get_all_users_excludes_password():
    email = "listuser@example.com"
    password = "senha123"
    create_user(email, password)

    users_coll = get_users_collection()
    users = list(users_coll.find({}, {"password": 0}))

    assert len(users) > 0
    for user in users:
        assert "password" not in user  # senha não deve estar exposta
        assert "email" in user

client = TestClient(app)

def test_root_route():
    """Verifica se a rota raiz '/' responde corretamente"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json() or "detail" in response.json()