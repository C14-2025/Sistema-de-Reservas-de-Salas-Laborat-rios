from ..database.db import get_database
from bson import ObjectId
from typing import Optional

def create_reservation(user_email: str, lab_id: str, date: str, start_time: str, end_time: str) -> dict:
    
    db = get_database()
    reservations_coll = db["reservations"]

    conflict = reservations_coll.find_one({
        "lab_id": lab_id,
        "date": date,
        "$or": [
            {"start_time": {"$lt": end_time, "$gte": start_time}},
            {"end_time": {"$gt": start_time, "$lte": end_time}}
        ]
    })

    if conflict:
        raise ValueError("Horário já reservado para este laboratório.")

    reservation = {
        "user_email": user_email,
        "lab_id": lab_id,
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

    conflict = reservations_coll.find_one({
        "lab_id": lab_id,
        "date": date,
        "$or": [
            {"start_time": {"$lt": end_time}},
            {"end_time": {"$gt": start_time}}
        ]
    })

    return conflict is None
