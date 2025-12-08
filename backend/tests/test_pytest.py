import pytest
from fastapi.testclient import TestClient
from passlib.hash import bcrypt

from backend.app.main import app
from backend.app.database.db import get_users_collection


@pytest.fixture()
def test_client():
    return TestClient(app)


def test_register_user(test_client):
    payload = {
        "name": "Teste",
        "email": "teste@email.com",
        "password": "123456"
    }

    response = test_client.post("/user/register", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["message"] == "Usuário criado com sucesso!"


def test_login_user(test_client):
    users_coll = get_users_collection()
    users_coll.delete_many({})

    users_coll.insert_one({
        "name": "Teste",
        "email": "teste@login.com",
        "password": bcrypt.hash("123456")
    })

    payload = {
        "email": "teste@login.com",
        "password": "123456"
    }

    response = test_client.post("/auth/login", json=payload)

    assert response.status_code == 200

