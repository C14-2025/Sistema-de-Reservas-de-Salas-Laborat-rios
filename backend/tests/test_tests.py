import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from backend.app.utils.auth import hash_password, create_user, users_coll

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
