import pytest
from backend.app.main import app
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from backend.app.routes.user import register_user  # CORREÇÃO: rota de user
from backend.app.models.user import UserCreate  # CORREÇÃO: classe correta

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_register_user_sucesso():
    user = UserCreate(name="Mock User", email="mockuser@example.com", password="123456")

    # cria mock da coleção
    users_coll_mock = MagicMock()
    users_coll_mock.find_one.return_value = None  # não achou email
    users_coll_mock.insert_one.return_value = MagicMock(inserted_id="123")

    # patcha o get_users_collection para devolver o mock
    with patch("backend.app.routes.user.get_users_collection", return_value=users_coll_mock):
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

# NOVA CONTRIBUIÇÃO (NP3) - OTÁVIO
def test_register_user_missing_fields(test_client):
    """
    Verifica se a API retorna erro 422 quando algum campo obrigatório
    não é enviado no JSON.
    """

    # Payload faltando campos importantes (faltando 'email' e 'password')
    payload = {
        "name": "Usuário Sem Email"
    }

    response = test_client.post("/user/register", json=payload)

    # O FastAPI automaticamente retorna 422 para validação inválida
    assert response.status_code == 422
    assert "detail" in response.json()

def test_auth_module_loads():
    """
    Teste mínimo e seguro: garante apenas que o módulo auth
    pode ser importado sem gerar erros.
    """
    try:
        import backend.app.routes.auth as auth_module
    except Exception as e:
        assert False, f"Falha ao importar módulo auth: {e}"

    # Se chegou até aqui, o teste passa
    assert True
