import pytest
import mongomock
from fastapi.testclient import TestClient
from passlib.hash import bcrypt

# IMPORTS DO SEU PROJETO (ajuste se necessário)
from backend.app.main import app
from backend.app.database.db import get_users_collection


# -------------------------------
# FIXTURES DO BANCO MOCKADO
# -------------------------------

@pytest.fixture(scope="session")
def mock_db():
    """Cria um banco MongoDB mockado (mongomock) para toda a suíte de testes."""
    client = mongomock.MongoClient()
    db = client["test_db"]
    return db


def override_get_users_collection_factory(mock_db):
    """Retorna função que substitui get_users_collection para usar o banco mockado."""
    def _override():
        return mock_db["users"]
    return _override


@pytest.fixture()
def test_client(mock_db):
    """Cria client do FastAPI para testes, com DB mockado."""
    # Override da dependência
    app.dependency_overrides[get_users_collection] = override_get_users_collection_factory(mock_db)

    client = TestClient(app)
    yield client

    # Remove override após o teste
    app.dependency_overrides.clear()



# -------------------------------
# TESTE: REGISTRO
# -------------------------------

def test_register_user(test_client):
    payload = {
        "name":"Teste",
        "email": "teste@email.com",
        "password": "123456"
    }

    response = test_client.post("/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["message"] == "Usuário registrado com sucesso"



# -------------------------------
# TESTE: LOGIN
# -------------------------------

def test_login_user(test_client, mock_db):
    """Testa login com senha criptografada."""


    mock_db["users"].insert_one({
    
        "email": "teste@login.com",
        "password": bcrypt.hash("123456")
    })

    payload = {
        "email": "teste@login.com",
        "password": "123456"
    }

    response = test_client.post("/auth/login", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["message"] == "Login bem-sucedido"
