from fastapi import APIRouter, HTTPException
from ..models.auth import LoginRequest, LoginResponse
from ..database.db import get_users_collection
from ..utils.auth import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login_user(credentials: LoginRequest):
    users_coll = get_users_collection()
    
    user_data = users_coll.find_one({"email": credentials.email})

    if not user_data or not verify_password(credentials.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return LoginResponse(
        id=str(user_data["_id"]),
        message="Login bem-sucedido"
    )
