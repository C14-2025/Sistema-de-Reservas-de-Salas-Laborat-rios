from fastapi import APIRouter, status, HTTPException
from typing import List
from ..models.lab import LabRegister, LabRegisterResponse, LabOut
from ..database.db import get_labs_collection
from ..utils.lab import create_lab

router = APIRouter(prefix="/labs", tags=["Labs"])

@router.post(
    "/register",
    response_model=LabRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_lab(lab: LabRegister):
    try:
        labs_coll = get_labs_collection()
        if labs_coll.find_one({"name": lab.name}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lab já cadastrado"
            )
        new_lab = create_lab(
            name=lab.name,
            description=lab.description or ""
        )

        return LabRegisterResponse(
            id=new_lab["_id"],
            name=new_lab["name"],
            description=new_lab.get("description")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[LabOut],
    status_code=status.HTTP_200_OK
)
async def list_labs():
    try:
        labs_coll = get_labs_collection()
        labs = list(labs_coll.find({}))

        for lab in labs:
            lab["_id"] = str(lab["_id"])

        return [
            LabOut(
                id=lab["_id"],
                name=lab["name"],
                description=lab.get("description")
            )
            for lab in labs
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )
