"""Tests for the processor logic"""
import pytest
from datetime import datetime
from app.logic.processor import get_validation_errors
from app.models import NormalizedEvent, SourceType, LanguageType


class TestGetValidationErrors:
    """Test suite for get_validation_errors function"""
    
    def test_valid_event_no_errors(self):
        """Test that a valid event returns no errors"""
        event = NormalizedEvent(
            event_id="evt_123",
            user_id="usr_456",
            source=SourceType.WEB,
            lang=LanguageType.ENGLISH,
            ts=datetime.fromisoformat("2024-02-13T10:30:00+00:00"),
            ref="Genesis 1:1"
        )
        
        errors = get_validation_errors(event.model_dump())
        
        assert errors == []
    
    def test_missing_user_id(self):
        """Test that missing user_id is detected"""
        event = {
            "event_id": "evt_123",
            "ref": "Genesis 1:1"
        }
        
        errors = get_validation_errors(event)
        
        assert "MISSING_USER_ID" in errors
    
    def test_missing_ref(self):
        """Test that missing ref is detected"""
        event = NormalizedEvent(
            event_id="evt_123",
            user_id="usr_456"
        )
        
        errors = get_validation_errors(event.model_dump())
        
        assert "NO_REFS" in errors
    
    def test_missing_both_user_id_and_ref(self):
        """Test that both missing user_id and ref are detected"""
        event = {
            "event_id": "evt_123"
        }
        
        errors = get_validation_errors(event)
        
        assert "MISSING_USER_ID" in errors
        assert "NO_REFS" in errors
    
    def test_invalid_source(self):
        """Test that invalid source is detected"""
        event = {
            "user_id": "usr_456",
            "source": "invalid_source",
            "ref": "Genesis 1:1"
        }
        
        errors = get_validation_errors(event)
        
        assert "INVALID_SOURCE" in errors
    
    def test_valid_source_values(self):
        """Test that valid source values are accepted"""
        for source in SourceType:
            event = NormalizedEvent(
                user_id="usr_456",
                source=source,
                ref="Genesis 1:1"
            )
            
            errors = get_validation_errors(event.model_dump())
            
            assert "INVALID_SOURCE" not in errors
    
    def test_invalid_lang(self):
        """Test that invalid language is detected"""
        event = {
            "user_id": "usr_456",
            "lang": "invalid_lang",
            "ref": "Genesis 1:1"
        }
        
        errors = get_validation_errors(event)
        
        assert "INVALID_LANG" in errors
    
    def test_valid_lang_values(self):
        """Test that valid language values are accepted"""
        for lang in LanguageType:
            event = NormalizedEvent(
                user_id="usr_456",
                lang=lang,
                ref="Genesis 1:1"
            )
            
            errors = get_validation_errors(event.model_dump())
            
            assert "INVALID_LANG" not in errors
    
    def test_invalid_ref(self):
        """Test that invalid ref format is detected"""
        event = {
            "user_id": "usr_456",
            "ref": "invalid_ref_format"
        }
        
        errors = get_validation_errors(event)
        
        assert "INVALID_REF" in errors
    
    def test_valid_ref_format(self):
        """Test that valid ref format is accepted"""
        event = NormalizedEvent(
            user_id="usr_456",
            ref="Genesis 1:1"
        )
        
        errors = get_validation_errors(event.model_dump())
        
        assert "INVALID_REF" not in errors
    
    def test_malformed_timestamp(self):
        """Test that malformed timestamp is detected"""
        event = {
            "user_id": "usr_456",
            "ts": "not-a-valid-timestamp",
            "ref": "Genesis 1:1"
        }
        
        errors = get_validation_errors(event)
        
        assert "BAD_TIMESTAMP" in errors
    
    def test_valid_iso_timestamp(self):
        """Test that valid ISO timestamp is accepted"""
        event = NormalizedEvent(
            user_id="usr_456",
            ts=datetime.fromisoformat("2024-02-13T10:30:00+00:00"),
            ref="Genesis 1:1"
        )
        
        errors = get_validation_errors(event.model_dump())
        
        assert "BAD_TIMESTAMP" not in errors
    
    def test_valid_iso_timestamp_with_offset(self):
        """Test that ISO timestamp with offset is accepted"""
        event = {
            "user_id": "usr_456",
            "ts": "2024-02-13T10:30:00+05:00",
            "ref": "Genesis 1:1"
        }
        
        errors = get_validation_errors(event)
        
        assert "BAD_TIMESTAMP" not in errors
    
    def test_multiple_errors(self):
        """Test that all errors are detected in one event"""
        event = {
            "source": "invalid",
            "lang": "invalid",
            "ts": "bad-ts"
        }
        
        errors = get_validation_errors(event)
        
        assert "MISSING_USER_ID" in errors
        assert "NO_REFS" in errors
        assert "INVALID_SOURCE" in errors
        assert "INVALID_LANG" in errors
        assert "BAD_TIMESTAMP" in errors
