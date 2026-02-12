from typing import Any, Dict, List, Optional
from app.models import NormalizedEvent, SourceType, LanguageType
from app.validators import validate_source, validate_lang, validate_ref


def get_validation_errors(event_dict: Dict[str, Any]) -> List[str]:
    """Check an event for validation errors and return list of error codes"""
    errors = []
    
    # Check required fields
    if not event_dict.get("user_id"):
        errors.append("MISSING_USER_ID")
    
    if not event_dict.get("ref"):
        errors.append("NO_REFS")
    
    # Validate source
    if event_dict.get("source"):
        try:
            validate_source(event_dict.get("source"))
        except ValueError:
            errors.append("INVALID_SOURCE")
    
    # Validate language
    if event_dict.get("lang"):
        try:
            validate_lang(event_dict.get("lang"))
        except ValueError:
            errors.append("INVALID_LANG")
    
    # Validate reference
    if event_dict.get("ref"):
        try:
            validate_ref(event_dict.get("ref"))
        except ValueError:
            errors.append("INVALID_REF")
    
    # Validate timestamp
    if event_dict.get("ts"):
        try:
            # If ts is a string, try to parse it
            if isinstance(event_dict.get("ts"), str):
                from datetime import datetime
                datetime.fromisoformat(event_dict.get("ts").replace('Z', '+00:00'))
        except Exception:
            errors.append("BAD_TIMESTAMP")
    
    return errors


def try_parse_event(event_dict: Dict[str, Any]) -> Optional[NormalizedEvent]:
    """Try to parse dict into NormalizedEvent model"""
    try:
        return NormalizedEvent(**event_dict)
    except Exception:
        return None
