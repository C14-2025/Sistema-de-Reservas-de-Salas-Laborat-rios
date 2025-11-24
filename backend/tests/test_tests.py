import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi.testclient import TestClient
from backend.app.main import app


# 🔥 FIXTURE GLOBAL: mocka totalmente o MongoDB
@pytest.fixture(scope="session", autouse=True)
def mock_mongo():
    fake_db = MagicMock()
    fake_users = {}
    fake_labs = {}
    fake_reservations = {}

    # --- simulando coleções ---
    fake_db.__getitem__.side_effect = lambda name: {
        "users": fake_users,
        "labs": fake_labs,
        "reservations": fake_reservations
    }[name]

    # Métodos simulados
    def fake_insert_one(collection):
        def _insert_one(doc):
            _id = str(len(collection) + 1)
            doc["_id"] = _id
            collection[_id] = doc
            return MagicMock(inserted_id=_id)
        return _insert_one

    def fake_find_one(collection):
        return lambda query: next(
            (doc for doc in collection.values() if all(doc.get(k) == v for k, v in query.items())),
            None
        )

    def fake_delete_many(collection):
        return lambda _: collection.clear()

    def fake_find(collection):
        return lambda *args, **kwargs: list(collection.values())

    # atribuições
    fake_db["users"].insert_one = fake_insert_one(fake_users)
    fake_db["users"].delete_many = fake_delete_many(fake_users)
    fake_db["users"].find_one = fake_find_one(fake_users)
    fake_db["users"].find = fake_find(fake_users)

    fake_db["labs"].insert_one = fake_insert_one(fake_labs)
    fake_db["labs"].delete_many = fake_delete_many(fake_labs)
    fake_db["labs"].find = fake_find(fake_labs)
    fake_db["labs"].find_one = fake_find_one(fake_labs)

    fake_db["reservations"].insert_one = fake_insert_one(fake_reservations)
    fake_db["reservations"].delete_many = fake_delete_many(fake_reservations)
    fake_db["reservations"].find = fake_find(fake_reservations)
    fake_db["reservations"].find_one = fake_find_one(fake_reservations)

    # Patcha todas as funções que buscam o banco real
    with patch("app.database.db.get_database", return_value=fake_db):
        with patch("app.database.db.get_users_collection", return_value=fake_db["users"]):
            with patch("app.database.db.get_labs_collection", return_value=fake_db["labs"]):
                with patch("app.database.db.get_reservations_collection", return_value=fake_db["reservations"]):
                    yield


# -----------------------------------------------------------
# Agora os testes abaixo funcionam normalmente SEM Mongo real
# -----------------------------------------------------------

client = TestClient(app)

def test_create_user():
    from app.utils.auth import create_user, verify_password
    email = "teste@example.com"
    password = "123456"

    create_user(email, password)
    users = client.app.state._state["db"]["users"]

    assert users["1"]["email"] == email
    assert verify_password(password, users["1"]["password"])


def test_duplicate_email():
    from app.utils.auth import create_user
    email = "dup@example.com"

    create_user(email, "123")
    with pytest.raises(ValueError):
        create_user(email, "123")


def test_password_hashed():
    from app.utils.auth import hash_password
    hashed = hash_password("123456")
    assert hashed != "123456"


def test_login_valid_user():
    from app.utils.auth import create_user, verify_password
    email = "valid@example.com"
    create_user(email, "abc123")

    users = client.app.state._state["db"]["users"]
    assert verify_password("abc123", users["1"]["password"])


def test_root_route():
    r = client.get("/")
    assert r.status_code == 200


def test_create_reservation_success():
    from app.utils.reservation import create_reservation
    from app.database.db import get_labs_collection

    labs = get_labs_collection()
    lab = {"name": "Lab Teste"}
    lab_id = labs.insert_one(lab).inserted_id

    res = create_reservation("u@inatel.br", lab_id, "2025-01-01", "10:00", "11:00")

    assert res["_id"] is not None
    assert res["lab_id"] == lab_id


def test_create_reservation_conflict():
    from app.utils.reservation import create_reservation
    from app.database.db import get_labs_collection

    labs = get_labs_collection()
    lab_id = labs.insert_one({"name": "Lab"}).inserted_id

    create_reservation("u1@inatel.br", lab_id, "2025-01-01", "10:00", "12:00")

    with pytest.raises(ValueError):
        create_reservation("u2@inatel.br", lab_id, "2025-01-01", "11:00", "12:30")

