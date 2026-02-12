from fastapi import APIRouter
from typing import List, Any, Dict
from app.models import ProcessingResult
from app.logic.processor import get_validation_errors
from app.models import NormalizedEvent

router = APIRouter()


@router.post("/process")
def process_data(items: List[Dict[str, Any]]):
    """Process and validate an array of events"""
    result = ProcessingResult()
    result.set_total_in(len(items))
    
    for item in items:
        errors = get_validation_errors(item)
        
        if errors:
            # Event has validation errors - quarantine it
            result.add_quarantined(item, errors)
        else:
            # Event is valid - normalize it
            event = NormalizedEvent(**item)
            result.add_normalized(event.model_dump())
    
    return result.to_dict()
