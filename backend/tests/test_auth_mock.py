import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.routes.user import register_user  # CORREÇÃO: rota de user
from app.models.user import UserCreate  # CORREÇÃO: classe correta

@pytest.mark.asyncio
async def test_register_user_sucesso():
    user = UserCreate(name="Mock User", email="mockuser@example.com", password="123456")

    # cria mock da coleção
    users_coll_mock = MagicMock()
    users_coll_mock.find_one.return_value = None  # não achou email
    users_coll_mock.insert_one.return_value = MagicMock(inserted_id="123")

    # patcha o get_users_collection para devolver o mock
    with patch("app.routes.user.get_users_collection", return_value=users_coll_mock):
        result = await register_user(user)

    assert result.email == user.email
    assert result.message == "Usuário criado com sucesso!"
    users_coll_mock.find_one.assert_called_once_with({"email": user.email})
    users_coll_mock.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_email_existente():
    user = UserCreate(name="Mock User", email="mockuser@example.com", password="123456")

    users_coll_mock = MagicMock()
    users_coll_mock.find_one.return_value = {"email": user.email}

    with patch("backend.app.routes.user.get_users_collection", return_value=users_coll_mock):
        with pytest.raises(HTTPException) as excinfo:
            await register_user(user)

    assert excinfo.value.status_code == 400
    users_coll_mock.find_one.assert_called_once_with({"email": user.email})
    users_coll_mock.insert_one.assert_not_called()
