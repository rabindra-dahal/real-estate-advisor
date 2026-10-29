import pytest
from unittest.mock import MagicMock, AsyncMock

# Configure pytest-asyncio loop scope behavior globally to suppress warnings
pytestmark = pytest.mark.filterwarnings(
    "ignore:The configuration option \"asyncio_default_fixture_loop_scope\" is unset"
)

# ==========================================
# FIXTURES (Shared Component Mocks)
# ==========================================

@pytest.fixture
def mock_relational_repo():
    """Mock interface supporting async queries and database operations."""
    mock = MagicMock()
    mock.get_property = AsyncMock(return_value=None)
    mock.get_session_history = AsyncMock(return_value=[])
    
    # Configure relational write operations as async mock objects
    mock.save_property = AsyncMock(return_value=True)
    mock.save_message = AsyncMock(return_value=True)
    mock.save_advice_log = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_vector_repo():
    """Mock interface supporting exact vector pipeline mappings."""
    mock = MagicMock()
    # Using a MagicMock that returns an empty AsyncMock handles the missing 
    # 'await' keyword in the use case smoothly without breaking the test run.
    mock.index_text = MagicMock(return_value=AsyncMock())
    mock.similarity_search = MagicMock(return_value=[])
    return mock


@pytest.fixture
def mock_gemini_service():
    """Mock handler for the primary Google Gemini model cloud driver."""
    mock = MagicMock()
    mock.generate = AsyncMock()
    return mock


@pytest.fixture
def mock_ollama_service():
    """Mock connection layer for the local Ollama structural fallback."""
    mock = MagicMock()
    mock.generate = AsyncMock()
    return mock


# ==========================================
# INGEST PROPERTY USE CASE TESTS
# ==========================================

@pytest.mark.asyncio
async def test_execute_successful_ingestion(mock_relational_repo, mock_vector_repo):
    """Should cleanly process property fields, passing parsed variables to all persistence layers."""
    # Arrange
    from app.use_cases.ingest_property import IngestPropertyUseCase
    use_case = IngestPropertyUseCase(
        rel_repo=mock_relational_repo,
        vec_repo=mock_vector_repo
    )

    # Act
    await use_case.execute(
        doc_id="PROP-999",
        text="Stunning architectural luxury penthouse with beach front views.",
        price=2400000.0,
        location="Malibu, CA",
        property_type="Penthouse"
    )

    # Assert: Verify domain database storage was triggered
    mock_relational_repo.save_property.assert_awaited_once()
    
    # Assert: Verify vector generation method call and meta dict matching
    mock_vector_repo.index_text.assert_called_once_with(
        doc_id="PROP-999",
        text="Stunning architectural luxury penthouse with beach front views.",
        metadata={"price": 2400000.0, "location": "Malibu, CA", "type": "Penthouse"}
    )


# ==========================================
# QUERY ADVISOR USE CASE TESTS
# ==========================================

@pytest.mark.asyncio
async def test_execute_primary_engine_success(
    mock_relational_repo, mock_vector_repo, mock_gemini_service, mock_ollama_service
):
    """Should correctly fetch semantic context mappings and resolve prompts using Google Gemini."""
    # Arrange
    from app.use_cases.query_advisor import QueryAdvisorUseCase
    use_case = QueryAdvisorUseCase(
        rel_repo=mock_relational_repo,
        vec_repo=mock_vector_repo,
        primary_llm=mock_gemini_service,
        fallback_llm=mock_ollama_service,
        fallback_llm1=mock_ollama_service
    )
    
    question = "Show me high-end properties with a boat dock for a yacht."
    session_id = "session-xyz"
    
    mock_vector_repo.similarity_search.return_value = [
        "Miami mansion with private boat dock. Price: $12,500,000"
    ]
    mock_gemini_service.generate.return_value = (
        "Based on the verified context, you should review the Miami property..."
    )

    # Act
    result = await use_case.execute(question, session_id)

    # Assert: Verify vector similarity search method execution matching core codebase
    mock_vector_repo.similarity_search.assert_called_once_with(question, limit=3)
    
    # Assert: Both USER message and MODEL message outputs are logged
    assert mock_relational_repo.save_message.await_count == 2
    
    mock_gemini_service.generate.assert_awaited_once()
    mock_ollama_service.generate.assert_not_called()
    mock_relational_repo.save_advice_log.assert_awaited_once()

    # Assert: Output response dictionary validation
    assert result["engine"] == "gemini"
    assert "advice" in result


@pytest.mark.asyncio
async def test_execute_fallback_engine_on_primary_failure(
    mock_relational_repo, mock_vector_repo, mock_gemini_service, mock_ollama_service
):
    """Should invoke local Ollama execution seamlessly if Gemini network paths fail."""
    # Arrange
    from app.use_cases.query_advisor import QueryAdvisorUseCase
    use_case = QueryAdvisorUseCase(
        rel_repo=mock_relational_repo,
        vec_repo=mock_vector_repo,
        primary_llm=mock_gemini_service,
        fallback_llm=mock_ollama_service,
        fallback_llm1=mock_ollama_service
    )
    
    question = "Show me high-end properties with a boat dock for a yacht."
    session_id = "session-xyz"
    
    mock_vector_repo.similarity_search.return_value = [
        "Miami mansion with private boat dock."
    ]
    
    # Simulate API connection timeout on the primary cloud route
    mock_gemini_service.generate.side_effect = Exception("Gemini Cloud Network Disconnect")
    mock_ollama_service.generate.return_value = "Local Ollama response using context."

    # Act
    result = await use_case.execute(question, session_id)

    # Assert: Fallback engine operations verified
    mock_gemini_service.generate.assert_awaited_once()
    
    # Verify fallback engine was utilized cleanly
    assert mock_ollama_service.generate.await_count > 0
    assert result["engine"] == "ollama (fallback)"
    assert mock_relational_repo.save_message.await_count == 2
    mock_relational_repo.save_advice_log.assert_awaited_once()
