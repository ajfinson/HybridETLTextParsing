"""Tests for the ProcessingResult model"""
import pytest
from app.models import ProcessingResult


class TestProcessingResult:
    """Test suite for ProcessingResult class"""
    
    def test_initialization(self):
        """Test ProcessingResult initializes with correct default values"""
        result = ProcessingResult()
        
        assert result.normalized == []
        assert result.quarantined == []
        assert result.stats["total_in"] == 0
        assert result.stats["total_out"] == 0
        assert result.stats["total_quarantined"] == 0
        assert result.stats["errors_by_type"] == {}
    
    def test_add_normalized_event(self):
        """Test adding a normalized event"""
        result = ProcessingResult()
        event = {"event_id": "evt_001", "user_id": "usr_001"}
        
        result.add_normalized(event)
        
        assert len(result.normalized) == 1
        assert result.normalized[0] == event
        assert result.stats["total_out"] == 1
    
    def test_add_multiple_normalized_events(self):
        """Test adding multiple normalized events"""
        result = ProcessingResult()
        events = [
            {"event_id": "evt_001"},
            {"event_id": "evt_002"},
            {"event_id": "evt_003"}
        ]
        
        for event in events:
            result.add_normalized(event)
        
        assert len(result.normalized) == 3
        assert result.stats["total_out"] == 3
    
    def test_add_quarantined_event(self):
        """Test adding a quarantined event"""
        result = ProcessingResult()
        raw_event = {"event_id": "evt_001"}
        errors = ["MISSING_USER_ID", "NO_REFS"]
        
        result.add_quarantined(raw_event, errors)
        
        assert len(result.quarantined) == 1
        assert result.quarantined[0]["raw"] == raw_event
        assert result.quarantined[0]["errors"] == errors
        assert result.stats["total_quarantined"] == 1
    
    def test_error_count_tracking(self):
        """Test that error counts are tracked correctly"""
        result = ProcessingResult()
        
        result.add_quarantined({"event_id": "evt_001"}, ["MISSING_USER_ID"])
        result.add_quarantined({"event_id": "evt_002"}, ["MISSING_USER_ID", "NO_REFS"])
        result.add_quarantined({"event_id": "evt_003"}, ["NO_REFS"])
        
        assert result.stats["errors_by_type"]["MISSING_USER_ID"] == 2
        assert result.stats["errors_by_type"]["NO_REFS"] == 2
        assert result.stats["total_quarantined"] == 3
    
    def test_set_total_in(self):
        """Test setting total_in count"""
        result = ProcessingResult()
        
        result.set_total_in(42)
        
        assert result.stats["total_in"] == 42
    
    def test_to_dict(self):
        """Test converting result to dictionary"""
        result = ProcessingResult()
        result.set_total_in(3)
        result.add_normalized({"event_id": "evt_001"})
        result.add_quarantined({"event_id": "evt_002"}, ["MISSING_USER_ID"])
        
        result_dict = result.to_dict()
        
        assert "normalized" in result_dict
        assert "quarantined" in result_dict
        assert "stats" in result_dict
        assert result_dict["stats"]["total_in"] == 3
        assert result_dict["stats"]["total_out"] == 1
        assert result_dict["stats"]["total_quarantined"] == 1
