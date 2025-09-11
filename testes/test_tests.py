import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from  backend import hash_password, create_user, verify_password, users_coll, authenticate_user, delete_user

@pytest.fixture(autouse=True)
def clear_db():
    users_coll.delete_many({})
    yield
    users_coll.delete_many({})

# Teste: cadastro de usuário válido
def test_create_user():
    email = "teste@example.com"
    password = "123456"
    user = create_user(email, password)
    
    db_user = users_coll.find_one({"email": email})
    assert db_user is not None
    assert db_user["email"] == email

#Teste: cadastro com email duplicado
def test_duplicate_email():
    email = "teste@example.com"
    password = "123456"
    create_user(email, password)
    
    with pytest.raises(ValueError):
        create_user(email, password)

#Teste: senha é realmente hasheada
def test_password_hashed():
    password = "123456"
    hashed = hash_password(password)
    
    assert hashed != password
    assert isinstance(hashed, str)

#Teste: Autentição usuário
def test_authenticate_user_success():
    email = "teste@example.com"
    password = "123456"
    create_user(email, password)

    user = authenticate_user(email, password)
    assert user is not None
    assert user["email"] == email
    assert verify_password(password, user["password"])

def test_authenticate_user_wrong_password():
    email = "teste@example.com"
    password = "123456"
    create_user(email, password)

    user = authenticate_user(email, "senha_errada")
    assert user is None

def test_authenticate_user_nonexistent_email():
    user = authenticate_user("naoexiste@example.com", "123456")
    assert user is None

#Teste: delete user
def test_delete_existing_user():
    email = "teste@example.com"
    password = "123456"
    create_user(email, password)

    deleted = delete_user(email)
    assert deleted is True
    assert users_coll.find_one({"email": email}) is None

def test_delete_nonexistent_user():
    deleted = delete_user("inexistente@example.com")
    assert deleted is False