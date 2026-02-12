from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class SourceType(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    PARTNER = "partner"


class LanguageType(str, Enum):
    ENGLISH = "en"
    HEBREW = "he"


class NormalizedEvent(BaseModel):
    event_id: Optional[str] = None
    user_id: Optional[str] = None
    source: Optional[SourceType] = None
    lang: Optional[LanguageType] = None
    ts: Optional[datetime] = None
    ref: Optional[str] = None


class DataItem(BaseModel):
    key: str
    value: str
