from fastapi import APIRouter
from typing import List
from app.models import NormalizedEvent
from app.validators import validate_event

router = APIRouter()


@router.post("/process")
def process_data(items: List[NormalizedEvent]):
    """Process and validate an array of normalized events"""
    for item in items:
        validate_event(item)
    
    if len(items) > 0:
        return {"status": "success"}
    return {"status": "failed"}
