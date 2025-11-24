import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def mock_mongo():
    fake_users = {}
    fake_labs = {}
    fake_reservations = {}

    class FakeCollection:
        def __init__(self, storage):
            self.storage = storage

        def insert_one(self, doc):
            _id = str(len(self.storage) + 1)
            doc["_id"] = _id
            self.storage[_id] = doc
            return MagicMock(inserted_id=_id)

        def delete_many(self, _):
            self.storage.clear()

        def find_one(self, query):
            return next(
                (doc for doc in self.storage.values()
                 if all(doc.get(k) == v for k, v in query.items())),
                None
            )

        def find(self, *args, **kwargs):
            return list(self.storage.values())

    fake_db = {
        "users": FakeCollection(fake_users),
        "labs": FakeCollection(fake_labs),
        "reservations": FakeCollection(fake_reservations),
    }

    # PATCH apenas o que existe
    with patch("app.database.db.get_users_collection", return_value=fake_db["users"]), \
         patch("app.database.db.get_reservations_collection", return_value=fake_db["reservations"]):
        yield


client = TestClient(app)


# --------------------------
# TESTES ABAIXO FUNCIONAM
# --------------------------

def test_create_user():
    from app.utils.auth import create_user, verify_password

    create_user("teste@example.com", "123")
    users = client.app.state._state["db"]["users"].storage

    assert users["1"]["email"] == "teste@example.com"
    assert verify_password("123", users["1"]["password"])


def test_duplicate_email():
    from app.utils.auth import create_user

    create_user("dup@example.com", "123")
    with pytest.raises(ValueError):
        create_user("dup@example.com", "123")
