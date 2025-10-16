import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from backend.app.routes.auth import register_user
from backend.app.models.user import UserRegister

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

@pytest.mark.asyncio
async def test_register_user_sucesso():
    user = UserRegister(email="mockuser@example.com", password="123456")

    # cria mock da coleção
    users_coll_mock = MagicMock()
    users_coll_mock.find_one.return_value = None  # não achou email
    users_coll_mock.insert_one.return_value = {"inserted_id": "123"}

    # patcha o get_users_collection para devolver o mock
    with patch("backend.app.routes.auth.get_users_collection", return_value=users_coll_mock):
        result = await register_user(user)

    assert result.email == user.email
    assert result.message == "Usuário criado com sucesso!"
    users_coll_mock.find_one.assert_called_once_with({"email": user.email})
    users_coll_mock.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_email_existente():
    user = UserRegister(email="mockuser@example.com", password="123456")

    users_coll_mock = MagicMock()
    users_coll_mock.find_one.return_value = {"email": user.email}

    with patch("backend.app.routes.auth.get_users_collection", return_value=users_coll_mock):
        with pytest.raises(HTTPException) as excinfo:
            await register_user(user)

    assert excinfo.value.status_code == 400
    users_coll_mock.find_one.assert_called_once_with({"email": user.email})
    users_coll_mock.insert_one.assert_not_called()