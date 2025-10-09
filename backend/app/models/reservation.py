from pydantic import BaseModel, Field
from typing import Optional

class ReservationBase(BaseModel):
    user_email: str
    lab_id: str
    date: str  # formato: YYYY-MM-DD
    start_time: str  # formato: HH:MM
    end_time: str  # formato: HH:MM
    status: Optional[str] = Field(default="pendente", description="Status da reserva")

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(BaseModel):
    message: str

class ReservationOut(ReservationBase):
    id: str
