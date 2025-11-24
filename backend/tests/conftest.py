import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="session", autouse=True)
def mock_mongo():
    # Armazenamento falso para as coleções
    fake_users = {}
    fake_labs = {}
    fake_reservations = {}

    # Classe FakeCollection para simular operações básicas do MongoDB
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

    # Banco de dados fake
    fake_db = {
        "users": FakeCollection(fake_users),
        "labs": FakeCollection(fake_labs),
        "reservations": FakeCollection(fake_reservations),
    }

    # PATCH para o módulo correto (database.db)
    with patch("app.database.db.get_users_collection", return_value=fake_db["users"]), \
         patch("app.database.db.get_labs_collection", return_value=fake_db["labs"]), \
         patch("app.database.db.get_reservations_collection", return_value=fake_db["reservations"]), \
         patch("app.database.db.get_database", return_value={
             "users": fake_db["users"],
             "labs": fake_db["labs"],
             "reservations": fake_db["reservations"]
         }):
        yield
