import pytest
from datetime import date
from unittest.mock import patch, MagicMock

from modules.metadata.base import MetadataResult, MetadataProvider


@pytest.fixture
def mock_metadata_result():
    """Create a mock metadata result for testing"""
    return MetadataResult(
        id="123",
        title="Test Title",
        original_title="Original Title",
        overview="Test Overview",
        release_date=date(2024, 1, 1),
        language="en",
    )


@pytest.fixture
def mock_provider():
    """Create a mock metadata provider for testing"""
    provider = MagicMock(spec=MetadataProvider)
    provider.search.return_value = []
    provider.get_by_id.return_value = None
    provider.get_external_ids.return_value = {}
    provider.get_keywords.return_value = []
    provider.get_trailers.return_value = []
    return provider


@pytest.fixture
def mock_requests():
    """Create a mock requests module for testing"""
    with patch("requests.get") as mock_get, patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        yield {"get": mock_get, "post": mock_post}


@pytest.fixture
def mock_jikan():
    """Create a mock Jikan client for testing"""
    with patch("jikanpy.Jikan") as mock_jikan:
        mock_instance = MagicMock()
        mock_instance.search.return_value = {"results": []}
        mock_instance.anime.return_value = {}
        mock_jikan.return_value = mock_instance
        yield mock_instance


@pytest.fixture(autouse=True)
def mock_logging():
    """Mock logging to prevent actual log output during tests"""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger


@pytest.fixture(autouse=True)
def mock_config():
    """Mock configuration settings for testing"""
    with patch("modules.config.UploaderConfig") as mock_uploader_config, patch(
        "modules.config.BaseUrlConfig"
    ) as mock_base_url_config:
        mock_uploader_config.return_value = MagicMock(
            tmdb_api_key="test_tmdb_key",
            imdb_api_key="test_imdb_key",
            tvdb_api_key="test_tvdb_key",
            anidb_api_key="test_anidb_key",
            mal_api_key="test_mal_key",
            anilist_client_id="test_anilist_id",
            anilist_client_secret="test_anilist_secret",
        )
        mock_base_url_config.return_value = MagicMock(
            tmdb_base_url="https://api.themoviedb.org/3",
            imdb_base_url="https://api.imdb.com",
            tvdb_base_url="https://api.thetvdb.com",
            anidb_base_url="https://api.anidb.net",
            tvmaze_base_url="https://api.tvmaze.com",
            mal_base_url="https://api.myanimelist.net/v2",
            anilist_base_url="https://graphql.anilist.co",
        )
        yield {
            "uploader": mock_uploader_config.return_value,
            "base_url": mock_base_url_config.return_value,
        }
