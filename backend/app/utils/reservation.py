from ..database.db import get_database
from bson import ObjectId
from typing import Optional
from ..utils.lab import get_lab_by_id

def _time_overlap(start_a: str, end_a: str, start_b: str, end_b: str) -> bool:
    return start_a < end_b and end_a > start_b

def create_reservation(user_email: str, lab_id: str, date: str, start_time: str, end_time: str) -> dict:
    db = get_database()
    reservations_coll = db["reservations"]
    lab = get_lab_by_id(lab_id)
    if not lab:
        raise ValueError("Laboratório não encontrado.")

    existing = list(reservations_coll.find({"lab_id": lab_id, "date": date}))
    for r in existing:
        r_start = r.get("start_time")
        r_end = r.get("end_time")
        if r_start is None or r_end is None:
            continue
        if _time_overlap(start_time, end_time, r_start, r_end):
            raise ValueError("Horário já reservado para este laboratório.")

    reservation = {
        "user_email": user_email,
        "lab_id": lab_id,
        "lab_name": lab.get("name", ""),
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "status": "pendente"
    }

    result = reservations_coll.insert_one(reservation)
    reservation["_id"] = str(result.inserted_id)

    return reservation


def get_all_reservations() -> list:
    db = get_database()
    reservations_coll = db["reservations"]

    reservations = list(reservations_coll.find({}))
    for r in reservations:
        r["_id"] = str(r["_id"])
    return reservations


def get_reservations_by_user(user_email: str) -> list:
    db = get_database()
    reservations_coll = db["reservations"]

    reservations = list(reservations_coll.find({"user_email": user_email}))
    for r in reservations:
        r["_id"] = str(r["_id"])
    return reservations


def get_reservation_by_id(reservation_id: str) -> Optional[dict]:
    db = get_database()
    reservations_coll = db["reservations"]

    reservation = reservations_coll.find_one({"_id": ObjectId(reservation_id)})
    if reservation:
        reservation["_id"] = str(reservation["_id"])
    return reservation


def check_availability(lab_id: str, date: str, start_time: str, end_time: str) -> bool:
    db = get_database()
    reservations_coll = db["reservations"]

    existing = list(reservations_coll.find({"lab_id": lab_id, "date": date}))
    for r in existing:
        r_start = r.get("start_time")
        r_end = r.get("end_time")
        if r_start is None or r_end is None:
            continue
        if _time_overlap(start_time, end_time, r_start, r_end):
            return False

    return True
