from fastapi import APIRouter, status, HTTPException
from typing import List
from ..models.user import LoginResponse, UserRegister, UserLogin, UserRegisterResponse, UserOut
from ..database.db import get_users_collection
from ..utils.auth import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user: UserRegister):
    try:
        users_coll = get_users_collection()
        if users_coll.find_one({"email": user.email}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        hashed_password = hash_password(user.password)
        new_user = {"email": user.email, "password": hashed_password}
        users_coll.insert_one(new_user)

        return UserRegisterResponse(
            email=user.email, message="Usuário criado com sucesso!"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email já cadastrado",
        )

@router.post("/login", response_model=LoginResponse)
async def login_user(user: UserLogin):
    try:
        users_coll = get_users_collection()
        user_data = users_coll.find_one({"email": user.email})
        if not user_data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not verify_password(user.password, user_data["password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return LoginResponse(email=user.email, message="Login bem-sucedido")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Credenciais inválidas",
        )

@router.get("/users")
async def get_all_users():
    try:
        users_coll = get_users_collection()
        users = list(users_coll.find({}, {"password": 0}))
        for user in users:
            user["_id"] = str(user["_id"])
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )
