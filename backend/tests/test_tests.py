import pytest
import asyncio

from app.utils.auth import hash_password, create_user, verify_password
from app.utils.lab import create_lab, get_all_labs, get_lab_by_id
from app.database.db import connect_to_mongo, close_connection_to_mongo, get_users_collection, get_labs_collection
from unittest.mock import MagicMock, patch
from app.utils.lab import create_lab, get_labs_collection

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
    labs_coll = get_labs_collection()
    labs_coll.delete_many({})
    yield
    users_coll.delete_many({})
    labs_coll.delete_many({})

# Teste: cadastro de usuário válido
def test_create_user_with_mock(mocker):
    fake_coll = MagicMock()
    mocker.patch("your_module.get_users_collection", return_value=fake_coll)

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


@patch("app.utils.lab.get_labs_collection")
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
