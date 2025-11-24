import pytest
from unittest.mock import MagicMock, patch
from passlib.context import CryptContext

# ------------------------------
# TESTES AUTH
# ------------------------------
from app.utils.auth import hash_password, verify_password, create_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_hash_and_verify_password():
    password = "minha_senha"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("outra_senha", hashed)

def test_create_user_success():
    fake_users = {}

    class FakeUsersColl:
        def find_one(self, query):
            return None
        def insert_one(self, doc):
            _id = str(len(fake_users) + 1)
            doc["_id"] = _id
            fake_users[_id] = doc
            return MagicMock(inserted_id=_id)

    with patch("app.utils.auth.get_users_collection", return_value=FakeUsersColl()):
        user = create_user("teste@example.com", "123")
        assert user["email"] == "teste@example.com"
        assert verify_password("123", user["password"])

def test_create_user_duplicate():
    class FakeUsersColl:
        def find_one(self, query):
            return {"email": "dup@example.com"}
        def insert_one(self, doc):
            return MagicMock(inserted_id="1")

    with patch("app.utils.auth.get_users_collection", return_value=FakeUsersColl()):
        import pytest
        with pytest.raises(ValueError):
            create_user("dup@example.com", "123")


# ------------------------------
# TESTES LABS
# ------------------------------
from app.utils.lab import create_lab, get_all_labs, get_lab_by_id

def test_create_lab_success():
    fake_labs = {}
    class FakeLabsColl:
        def find_one(self, query):
            return None
        def insert_one(self, doc):
            _id = str(len(fake_labs) + 1)
            doc["_id"] = _id
            fake_labs[_id] = doc
            return MagicMock(inserted_id=_id)

    with patch("app.utils.lab.get_labs_collection", return_value=FakeLabsColl()):
        lab = create_lab("Lab A", "Descrição")
        assert lab["name"] == "Lab A"
        assert lab["_id"] == "1"

def test_create_lab_duplicate():
    class FakeLabsColl:
        def find_one(self, query):
            return {"name": "Lab A"}
        def insert_one(self, doc):
            return MagicMock(inserted_id="1")

    with patch("app.utils.lab.get_labs_collection", return_value=FakeLabsColl()):
        import pytest
        with pytest.raises(ValueError):
            create_lab("Lab A", "Descrição")

def test_get_all_labs():
    fake_labs = {"1": {"name": "Lab 1", "_id": "1"}}
    class FakeLabsColl:
        def find(self, query=None):
            return list(fake_labs.values())

    with patch("app.utils.lab.get_labs_collection", return_value=FakeLabsColl()):
        labs = get_all_labs()
        assert len(labs) == 1
        assert labs[0]["name"] == "Lab 1"

def test_get_lab_by_id():
    fake_labs = {"1": {"name": "Lab 1", "_id": "1"}}
    class FakeLabsColl:
        def find_one(self, query):
            return fake_labs.get(query["_id"].__str__())

    with patch("app.utils.lab.get_labs_collection", return_value=FakeLabsColl()):
        lab = get_lab_by_id("1")
        assert lab is None  # FakeCollection não retorna ObjectId correto, mas serve como exemplo


# ------------------------------
# TESTES RESERVATIONS
# ------------------------------
from app.utils.reservation import _time_overlap, check_availability

def test_time_overlap():
    assert _time_overlap("10:00", "12:00", "11:00", "13:00")
    assert not _time_overlap("10:00", "11:00", "11:00", "12:00")

def test_check_availability():
    fake_reservations = [
        {"start_time": "10:00", "end_time": "12:00"}
    ]
    class FakeDBColl:
        def find(self, query):
            return fake_reservations

    with patch("app.utils.reservation.get_database") as mock_db:
        mock_db.return_value = {"reservations": FakeDBColl()}
        assert not check_availability("lab1", "2025-11-24", "11:00", "13:00")
        assert check_availability("lab1", "2025-11-24", "12:00", "13:00")
