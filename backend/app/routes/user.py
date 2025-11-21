from fastapi import APIRouter, status, HTTPException
from bson import ObjectId
from typing import List
from ..models.user import UserCreate, UserResponse
from ..database.db import get_users_collection
from ..utils.auth import hash_password

router = APIRouter(prefix="/user", tags=["Users"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user: UserCreate):
    users_coll = get_users_collection()

    if users_coll.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    hashed_password = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    }

    result = users_coll.insert_one(new_user)

    return UserResponse(
        id=str(result.inserted_id),
        name=user.name,
        email=user.email,
        message="Usuário criado com sucesso!"
    )

@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    users_coll = get_users_collection()

    users = []
    for user in users_coll.find({}, {"password": 0}):
        users.append(
            UserResponse(
                id=str(user["_id"]),
                name=user.get("name", ""),
                email=user["email"],
                message="Usuário encontrado"
            )
        )

    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str):
    users_coll = get_users_collection()

    try:
        oid = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    user = users_coll.find_one({"_id": oid}, {"password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return UserResponse(
        id=str(user["_id"]),
        name=user.get("name", ""),
        email=user["email"],
        message="Usuário encontrado"
    )
