from pydantic import BaseModel
from typing import Optional

class LabBase(BaseModel):
    name: str
    description: Optional[str] = None

class LabRegister(LabBase):
    pass

class LabRegisterResponse(LabBase):
    message: str

class LabOut(LabBase):
    id: str
