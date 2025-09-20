from ..database.db import get_labs_collection
from bson import ObjectId
from typing import Optional

def create_lab(name: str, description: str) -> dict:
  labs_coll = get_labs_collection()
  if labs_coll.find_one({"name": name}):
    raise ValueError("Lab já cadastrado")
  
  lab = {
    "name": name,
    "description": description,
  }
  result = labs_coll.insert_one(lab)
  lab["_id"] = str(result.inserted_id)

  return lab

def get_all_labs() -> list:
    labs_coll = get_labs_collection()
    labs = list(labs_coll.find({}))
    for lab in labs:
        lab["_id"] = str(lab["_id"])   

    return labs

def get_lab_by_id(lab_id: str) -> Optional[dict]:
    labs_coll = get_labs_collection()
    lab = labs_coll.find_one({"_id": ObjectId(lab_id)})
    if lab:
        lab["_id"] = str(lab["_id"])

    return lab
