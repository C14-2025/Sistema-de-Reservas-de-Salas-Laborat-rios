import pytest
import asyncio
from unittest.mock import MagicMock, patch

from backend.app.utils.auth import hash_password, create_user, verify_password
from backend.app.utils.lab import create_lab, get_all_labs, get_lab_by_id, get_labs_collection
from backend.app.utils.reservation import create_reservation, get_all_reservations, get_reservations_by_user, get_reservation_by_id, check_availability
from backend.app.database.db import connect_to_mongo, close_connection_to_mongo, get_users_collection, get_labs_collection, get_database

# Conecta no banco antes da sessão de testes e fecha no final
@pytest.fixture(scope="session", autouse=True)
def setup_mongo():
    asyncio.run(connect_to_mongo())
    yield
    asyncio.run(close_connection_to_mongo())

# Limpa a coleção de usuários antes e depois de cada teste
@pytest.fixture(autouse=True)
def clear_db():
    db = get_database()

    for name in db.list_collection_names():
        db[name].delete_many({})
    yield
    for name in db.list_collection_names():
        db[name].delete_many({})

# Teste: cadastro de usuário válido
def test_create_user_with_mock(mocker):
    fake_coll = MagicMock()
    mocker.patch("backend.app.utils.auth.get_users_collection", return_value=fake_coll)

    email = "teste@example.com"
    password = "123456"
    create_user(email, password)

    fake_coll.insert_one.assert_called_once()
    args, kwargs = fake_coll.insert_one.call_args
    assert kwargs["email"] == email

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


@patch("backend.app.utils.lab.get_labs_collection")
def test_create_lab_mock(mock_get_labs_collection):
    fake_coll = MagicMock()
    fake_coll.find_one.return_value = None
    fake_coll.insert_one.return_value.inserted_id = "mocked_id"
    mock_get_labs_collection.return_value = fake_coll
    lab_name = "Physics Lab"
    lab_description = "Lab for physics experiments"
    result = create_lab(lab_name, lab_description)
    fake_coll.insert_one.assert_called_once()
    assert result["_id"] == "mocked_id"
    assert result["name"] == lab_name
    assert result["description"] == lab_description

@patch("backend.app.utils.auth.get_users_collection")
def test_login_valid_user_mock(mock_get_users_collection):
    fake_coll = MagicMock()
    mock_get_users_collection.return_value = fake_coll

    email = "login@example.com"
    password = "senha123"
    hashed_password = "$2b$12$abcdefghijklmnopqrstuv"

    fake_coll.find_one.return_value = {"email": email, "password": hashed_password}

    user = fake_coll.find_one({"email": email})

    assert user is not None
    assert user["email"] == email
    assert user["password"] == hashed_password


def test_create_reservation_success():
    db = get_database()
    labs_coll = get_labs_collection()

    lab = {"name": "Lab Teste", "description": "Laboratório de testes"}
    lab_id = str(labs_coll.insert_one(lab).inserted_id)

    reservation = create_reservation(
        user_email="lucas.padua@inatel.br",
        lab_id=lab_id,
        date="2025-10-12",
        start_time="09:00",
        end_time="11:00",
    )

    assert reservation["_id"] is not None
    assert reservation["lab_id"] == lab_id
    assert reservation["user_email"] == "lucas.padua@inatel.br"
    assert reservation["status"] == "pendente"


def test_create_reservation_conflict():
    db = get_database()
    labs_coll = get_labs_collection()

    lab = {"name": "Lab Conflito", "description": "Teste de conflito"}
    lab_id = str(labs_coll.insert_one(lab).inserted_id)

    create_reservation(
        user_email="user1@inatel.br",
        lab_id=lab_id,
        date="2025-10-13",
        start_time="10:00",
        end_time="12:00",
    )

    with pytest.raises(ValueError):
        create_reservation(
            user_email="user2@inatel.br",
            lab_id=lab_id,
            date="2025-10-13",
            start_time="11:00",
            end_time="12:30",
        )


def test_check_availability_true():
    db = get_database()
    labs_coll = get_labs_collection()

    lab = {"name": "Lab Disponível", "description": "Teste de disponibilidade"}
    lab_id = str(labs_coll.insert_one(lab).inserted_id)

    available = check_availability(
        lab_id, "2025-10-14", "09:00", "10:00"
    )
    assert available is True


def test_check_availability_false():
    db = get_database()
    labs_coll = get_labs_collection()

    lab = {"name": "Lab Ocupado", "description": "Teste de conflito"}
    lab_id = str(labs_coll.insert_one(lab).inserted_id)

    create_reservation(
        user_email="user@inatel.br",
        lab_id=lab_id,
        date="2025-10-15",
        start_time="08:00",
        end_time="10:00",
    )

    available = check_availability(lab_id, "2025-10-15", "09:00", "09:30")
    assert available is False


def test_get_all_reservations_and_by_user():
    db = get_database()
    labs_coll = get_labs_collection()

    lab = {"name": "Lab Listagem", "description": "Teste de busca"}
    lab_id = str(labs_coll.insert_one(lab).inserted_id)

    create_reservation("user1@inatel.br", lab_id, "2025-10-16", "09:00", "10:00")
    create_reservation("user2@inatel.br", lab_id, "2025-10-17", "10:00", "11:00")

    all_res = get_all_reservations()
    assert len(all_res) == 2

    user1_res = get_reservations_by_user("user1@inatel.br")
    assert len(user1_res) == 1
    assert user1_res[0]["user_email"] == "user1@inatel.br"


def test_get_reservation_by_id():
    db = get_database()
    labs_coll = get_labs_collection()

    lab = {"name": "Lab ID", "description": "Teste de ID"}
    lab_id = str(labs_coll.insert_one(lab).inserted_id)

    created = create_reservation(
        "user@inatel.br", lab_id, "2025-10-18", "09:00", "10:00"
    )

    fetched = get_reservation_by_id(created["_id"])
    assert fetched is not None
    assert fetched["_id"] == created["_id"]
    assert fetched["lab_id"] == lab_id