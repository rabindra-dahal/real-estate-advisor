import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport

# Core application entry instance target sourced from root initialization definitions
from main import app
from app.use_cases.ingest_property import IngestPropertyUseCase

# Force all async tests in this module to evaluate via the anyio engine natively
pytestmark = pytest.mark.anyio


# ==========================================
# FIXTURES (Airtight Component Overrides)
# ==========================================

@pytest.fixture(autouse=True)
def fallback_infrastructure_overrides():
    """Mock the underlying repository methods globally to protect endpoints from database collisions."""
    mock_relational = MagicMock()
    mock_relational.get_property = AsyncMock(return_value=None)  # Guarantees new ingestion flows
    mock_relational.get_session_history = AsyncMock(return_value=[])
    mock_relational.save_property = AsyncMock(return_value=True)
    mock_relational.save_message = AsyncMock(return_value=True)
    mock_relational.save_advice_log = AsyncMock(return_value=True)

    mock_vector = MagicMock()
    mock_vector.index_text = AsyncMock(return_value=None)
    mock_vector.similarity_search = MagicMock(return_value=["Mocked Database Context"])

    # Map overrides directly to FastAPI dependency dictionary tables in case providers exist
    try:
        from app.delivery import dependencies as deps
        for name, attr in [(k, v) for k, v in vars(deps).items() if callable(v)]:
            if "relational" in name.lower() or "db" in name.lower():
                app.dependency_overrides[attr] = lambda: mock_relational
            elif "vector" in name.lower() or "vec" in name.lower() or "chroma" in name.lower():
                app.dependency_overrides[attr] = lambda: mock_vector
    except ImportError:
        pass


@pytest.fixture
def patch_ingest_use_case(monkeypatch):
    """Isolate the ingestion use case completely by monkeypatching its execute method at the class level."""
    mock_execute = AsyncMock(return_value=MagicMock())
    # Monkeypatch the actual execute method on the class to decouple it from underlying dependencies completely
    monkeypatch.setattr(IngestPropertyUseCase, "execute", mock_execute)
    return mock_execute


@pytest.fixture
async def client():
    """Asynchronous test client fixture configured to capture local router instances natively."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# ==========================================
# ENDPOINT INTEGRATION TESTS
# ==========================================

async def test_api_ingest_property_endpoint_success(client, patch_ingest_use_case):
    """POST /api/v3/properties should unpack payload and return a successful execution status."""
    # Arrange
    payload = {
        "doc_id": "PROP-999",
        "text": "Stunning architectural luxury penthouse with beach front views.",
        "price": 2400000.0,
        "location": "Malibu, CA",
        "property_type": "Penthouse"
    }

    # Act
    response = await client.post("/api/v3/properties", json=payload)
    
    # Assert successful status mapping codes (200, 201)
    assert response.status_code in (200, 201)
    
    # Verify the endpoint successfully parsed data and reached out to the correct execution block
    patch_ingest_use_case.assert_called_once()


async def test_api_ingest_property_validation_error(client):
    """POST /api/v3/properties should reject request payloads that don't match the required types."""
    # Arrange
    malformed_payload = {
        "doc_id": "PROP-999",
        "price": "not-a-float-number"  
    }

    # Act
    response = await client.post("/api/v3/properties", json=malformed_payload)
    
    # Assert
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()


async def test_api_execute_advisory_query_success(client):
    """POST /api/v3/advise should pipe user prompts down to the RAG generator and surface an execution matrix."""
    # Arrange
    payload = {
        "question": "Show me high-end properties with a boat dock for a yacht.",
        "session_id": "session-xyz"
    }

    # Act
    response = await client.post("/api/v3/advise", json=payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "advice" in data
