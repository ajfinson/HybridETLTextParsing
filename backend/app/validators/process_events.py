from app.models.process_data import SourceType, LanguageType


def validate_source(value):
    """Validate source field"""
    if value is not None and value not in [s.value for s in SourceType]:
        raise ValueError(f"source must be one of: {', '.join([s.value for s in SourceType])}")
    return value


def validate_lang(value):
    """Validate language field"""
    if value is not None and value not in [l.value for l in LanguageType]:
        raise ValueError(f"lang must be one of: {', '.join([l.value for l in LanguageType])}")
    return value


def validate_ref(value):
    """Validate reference field in canonical form"""
    if value is not None:
        # Basic canonical form validation: "Book Chapter:Verse[-Verse]"
        if not isinstance(value, str) or ":" not in value:
            raise ValueError("ref must be in canonical form (e.g., 'Genesis 1:1-3')")
    return value


def validate_event(event):
    """Validate a complete NormalizedEvent"""
    if event.source is not None:
        validate_source(event.source)
    if event.lang is not None:
        validate_lang(event.lang)
    if event.ref is not None:
        validate_ref(event.ref)
    return event
