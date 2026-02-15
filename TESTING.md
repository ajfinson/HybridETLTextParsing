# HybridETL Testing Guide

## Backend Tests

The backend uses **pytest** as the testing framework for the FastAPI application.

### Running Tests

```bash
# Install test dependencies
uv sync

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/routes/test_health.py

# Run tests matching a pattern
pytest -k "valid"

# Run with verbose output
pytest -v
```

### Test Structure

```
backend/
├── tests/
│   ├── conftest.py              # Pytest fixtures and configuration
│   ├── routes/
│   │   ├── test_health.py       # Health check endpoint tests
│   │   └── test_process.py      # Process endpoint tests
│   ├── logic/
│   │   └── test_processor.py    # Processor logic tests
│   └── models/
│       └── test_result.py       # ProcessingResult model tests
├── pytest.ini                    # Pytest configuration
└── requirements.txt              # Dependencies (includes pytest)
```

### Test Coverage

- **Routes**: Endpoint functionality, status codes, response formats
- **Logic**: Validation logic, error detection, data transformation
- **Models**: Data structures, method behavior

### Example Test

```python
def test_health_check(client):
    """Test that the health endpoint returns healthy status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

## Frontend Tests

Frontend tests can be added using testing frameworks like:
- **Jest** (recommended for JavaScript/React)
- **Vitest** (modern alternative for Vite projects)
- **Testing Library** (for component testing)

Placeholder directory: `frontend/tests/`

## Continuous Integration

To integrate tests into your CI/CD pipeline, add this to your workflow:

```bash
cd backend
pytest --tb=short
```

## Adding New Tests

1. Create a test file in the appropriate subdirectory
2. Name it `test_*.py`
3. Create test functions starting with `test_`
4. Use existing fixtures from `conftest.py` or create new ones
5. Run tests to verify
