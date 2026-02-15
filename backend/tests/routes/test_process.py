"""Tests for the process endpoint"""
import pytest
from datetime import datetime
from app.models import NormalizedEvent, SourceType, LanguageType


def test_process_valid_events(client):
    """Test processing valid events"""
    event = NormalizedEvent(
        event_id="evt_123",
        user_id="usr_456",
        source=SourceType.WEB,
        lang=LanguageType.ENGLISH,
        ts=datetime.fromisoformat("2024-02-13T10:30:00+00:00"),
        ref="Genesis 1:1"
    )
    response = client.post("/process", json=[event.model_dump(mode="json")])
    assert response.status_code == 200
    
    data = response.json()
    assert data["stats"]["total_in"] == 1
    assert data["stats"]["total_out"] == 1
    assert data["stats"]["total_quarantined"] == 0
    assert len(data["normalized"]) == 1
    assert len(data["quarantined"]) == 0


def test_process_invalid_events(client):
    """Test processing invalid events (missing user_id and ref)"""
    invalid_event = {
        "event_id": "evt_123",
        "source": "web",
        "lang": "en"
    }
    response = client.post("/process", json=[invalid_event])
    assert response.status_code == 200
    
    data = response.json()
    assert data["stats"]["total_in"] == 1
    assert data["stats"]["total_out"] == 0
    assert data["stats"]["total_quarantined"] == 1
    assert len(data["normalized"]) == 0
    assert len(data["quarantined"]) == 1
    assert "MISSING_USER_ID" in data["quarantined"][0]["errors"]
    assert "NO_REFS" in data["quarantined"][0]["errors"]


def test_process_mixed_batch(client):
    """Test processing a mixed batch of valid and invalid events"""
    valid_event_1 = NormalizedEvent(
        event_id="evt_001",
        user_id="usr_001",
        source=SourceType.WEB,
        lang=LanguageType.ENGLISH,
        ts=datetime.fromisoformat("2024-02-13T10:00:00+00:00"),
        ref="Genesis 1:1"
    )
    
    valid_event_2 = NormalizedEvent(
        event_id="evt_002",
        user_id="usr_002",
        source=SourceType.MOBILE,
        lang=LanguageType.HEBREW,
        ref="Exodus 2:5"
    )
    
    # Invalid event - missing required fields
    invalid_event = {
        "event_id": "evt_003",
        "source": "web"
    }
    
    batch = [
        valid_event_1.model_dump(mode="json"),
        valid_event_2.model_dump(mode="json"),
        invalid_event
    ]
    
    response = client.post("/process", json=batch)
    assert response.status_code == 200
    
    data = response.json()
    assert data["stats"]["total_in"] == 3
    assert data["stats"]["total_out"] == 2
    assert data["stats"]["total_quarantined"] == 1
    assert len(data["normalized"]) == 2
    assert len(data["quarantined"]) == 1


def test_process_empty_batch(client):
    """Test processing an empty batch"""
    response = client.post("/process", json=[])
    assert response.status_code == 200
    
    data = response.json()
    assert data["stats"]["total_in"] == 0
    assert data["stats"]["total_out"] == 0
    assert data["stats"]["total_quarantined"] == 0
    assert len(data["normalized"]) == 0
    assert len(data["quarantined"]) == 0


def test_process_invalid_source(client):
    """Test processing event with invalid source"""
    event = NormalizedEvent(
        event_id="evt_123",
        user_id="usr_456",
        source=SourceType.WEB,
        ref="Genesis 1:1"
    )
    # Manually set invalid source to bypass model validation
    event_dict = event.model_dump(mode="json")
    event_dict["source"] = "invalid_source"
    
    response = client.post("/process", json=[event_dict])
    assert response.status_code == 200
    
    data = response.json()
    assert data["stats"]["total_quarantined"] == 1
    assert "INVALID_SOURCE" in data["quarantined"][0]["errors"]


def test_process_invalid_lang(client):
    """Test processing event with invalid language"""
    event = NormalizedEvent(
        event_id="evt_123",
        user_id="usr_456",
        lang=LanguageType.ENGLISH,
        ref="Genesis 1:1"
    )
    # Manually set invalid lang to bypass model validation
    event_dict = event.model_dump(mode="json")
    event_dict["lang"] = "invalid_lang"
    
    response = client.post("/process", json=[event_dict])
    assert response.status_code == 200
    
    data = response.json()
    assert data["stats"]["total_quarantined"] == 1
    assert "INVALID_LANG" in data["quarantined"][0]["errors"]


def test_process_malformed_timestamp(client):
    """Test processing event with malformed timestamp"""
    event = {
        "event_id": "evt_123",
        "user_id": "usr_456",
        "ts": "not-a-timestamp",
        "ref": "Genesis 1:1"
    }
    response = client.post("/process", json=[event])
    assert response.status_code == 200
    
    data = response.json()
    assert data["stats"]["total_quarantined"] == 1
    assert "BAD_TIMESTAMP" in data["quarantined"][0]["errors"]
