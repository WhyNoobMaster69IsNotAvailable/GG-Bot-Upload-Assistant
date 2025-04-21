import pytest
from datetime import date
from unittest.mock import Mock, patch

from modules.metadata.base import MetadataResult, MetadataProvider
from modules.metadata.manager import MetadataService, MetadataManager


@pytest.fixture
def mock_metadata_result() -> MetadataResult:
    """Create a mock metadata result for testing"""
    return MetadataResult(
        id="123",
        title="Test Title",
        original_title="Original Title",
        overview="Test Overview",
        release_date=date(2024, 1, 1),
        language="en",
        external_ids={"imdb_id": "tt1234567"},
        keywords=["action", "drama"],
        trailers=["https://youtube.com/watch?v=abc123"],
    )


@pytest.fixture
def mock_provider() -> MetadataProvider:
    """Create a mock metadata provider for testing"""
    provider = Mock(spec=MetadataProvider)
    provider.search.return_value = []
    provider.get_by_id.return_value = None
    provider.get_external_ids.return_value = {}
    provider.get_keywords.return_value = []
    provider.get_trailers.return_value = []
    return provider


@pytest.fixture
def metadata_manager(mock_provider: MetadataProvider) -> MetadataManager:
    """Create a metadata manager with mock provider for testing"""
    manager = MetadataManager()
    manager.register_provider("mock", mock_provider)
    return manager


@pytest.fixture
def metadata_service(mock_provider: MetadataProvider) -> MetadataService:
    """Create a metadata service with mock provider for testing"""
    service = MetadataService()
    service.manager.providers["mock"] = mock_provider
    return service


@pytest.fixture
def mock_response() -> Mock:
    """Create a mock response for API testing"""
    response = Mock()
    response.ok = True
    response.json.return_value = {}
    return response


@pytest.fixture
def mock_requests(mock_response: Mock) -> Mock:
    """Create a mock requests module for API testing"""
    with patch("requests.get", return_value=mock_response) as mock_get, patch(
        "requests.post", return_value=mock_response
    ) as mock_post:
        yield {"get": mock_get, "post": mock_post}


@pytest.fixture
def mock_jikan() -> Mock:
    """Create a mock Jikan instance for MAL testing"""
    with patch("jikanpy.Jikan") as mock:
        instance = mock.return_value
        instance.search.return_value = {"results": []}
        instance.anime.return_value = {}
        yield instance
