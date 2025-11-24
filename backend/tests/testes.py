import pytest
import os
from database.db import (
    connect_to_mongo,
    close_connection_to_mongo,
    get_database,
    get_users_collection,
    get_labs_collection,
    get_reservations_collection,
)
from dotenv import load_dotenv
from pathlib import Path

# Carregar .env manualmente para teste
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


@pytest.mark.asyncio
async def test_env_variables():
    """Testa se as variáveis de ambiente estão carregadas"""
    assert os.getenv("MONGO_URI") is not None, "MONGO_URI não está definido"
    assert os.getenv("DB_NAME") is not None, "DB_NAME não está definido"


@pytest.mark.asyncio
async def test_connect_to_mongo():
    """Testa a conexão com o MongoDB"""
    result = await connect_to_mongo()
    assert result is True, "Falha ao conectar ao MongoDB"
    
    # Testa se as collections estão disponíveis
    db = get_database()
    users = get_users_collection()
    labs = get_labs_collection()
    reservations = get_reservations_collection()

    assert db.name == os.getenv("DB_NAME")
    assert users.name == "users"
    assert labs.name == "labs"
    assert reservations.name == "reservations"


@pytest.mark.asyncio
async def test_close_connection_to_mongo():
    """Testa o fechamento da conexão com MongoDB"""
    await connect_to_mongo()
    result = await close_connection_to_mongo()
    assert result is True, "Falha ao fechar conexão MongoDB"
