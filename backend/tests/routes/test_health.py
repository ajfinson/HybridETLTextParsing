"""Tests for the health check endpoint"""
import pytest


def test_health_check(client):
    """Test that the health endpoint returns healthy status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_check_content_type(client):
    """Test that health endpoint returns JSON content type"""
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"
