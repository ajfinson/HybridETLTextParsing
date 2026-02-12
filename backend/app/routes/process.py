from fastapi import APIRouter
from typing import List
from app.models import DataItem

router = APIRouter()


@router.post("/process")
def process_data(items: List[DataItem]):
    """Process an array of JSON objects"""
    if len(items) > 0:
        return {"status": "success"}
    return {"status": "failed"}
