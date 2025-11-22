from fastapi import APIRouter, HTTPException, status
from ..models.reservation import ReservationCreate, ReservationResponse, ReservationOut
from ..utils.reservation import (
    create_reservation,
    get_all_reservations,
    get_reservations_by_user,
    get_reservation_by_id,
    check_availability,
)
router = APIRouter(prefix="/reservations", tags=["Reservas"])

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_new_reservation(reservation: ReservationCreate):
    try:
        available = check_availability(
            reservation.lab_id,
            reservation.date,
            reservation.start_time,
            reservation.end_time,
        )

        if not available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Horário indisponível para este laboratório.",
            )

        new_reservation = create_reservation(
            reservation.user_email,
            reservation.lab_id,
            reservation.date,
            reservation.start_time,
            reservation.end_time,
        )

        return ReservationResponse(message="Reserva criada com sucesso!")

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )

@router.get("/", response_model=list[ReservationOut])
def list_all_reservations():
    try:
        reservations = get_all_reservations()
        formatted = [
            ReservationOut(
                id=r["_id"],
                user_email=r["user_email"],
                lab_id=r["lab_id"],
                lab_name=r.get("lab_name"),
                date=r["date"],
                start_time=r["start_time"],
                end_time=r["end_time"],
                status=r.get("status", "pendente"),
            )
            for r in reservations
        ]
        return formatted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{email}", response_model=list[ReservationOut])
def list_reservations_by_user(email: str):
    try:
        reservations = get_reservations_by_user(email)
        formatted = [
            ReservationOut(
                id=r["_id"],
                user_email=r["user_email"],
                lab_id=r["lab_id"],
                lab_name=r.get("lab_name"),
                date=r["date"],
                start_time=r["start_time"],
                end_time=r["end_time"],
                status=r.get("status", "pendente"),
            )
            for r in reservations
        ]
        return formatted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{reservation_id}", response_model=ReservationOut)
def get_reservation(reservation_id: str):
    try:
        reservation = get_reservation_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reserva não encontrada.")

        return ReservationOut(
            id=reservation["_id"],
            user_email=reservation["user_email"],
            lab_id=reservation["lab_id"],
            lab_name=reservation.get("lab_name"),
            date=reservation["date"],
            start_time=reservation["start_time"],
            end_time=reservation["end_time"],
            status=reservation.get("status", "pendente"),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
