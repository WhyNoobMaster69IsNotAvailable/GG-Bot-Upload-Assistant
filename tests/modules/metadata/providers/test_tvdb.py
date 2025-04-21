import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.providers.tvdb import TVDBProvider
from modules.metadata.base import MetadataResult


@pytest.fixture
def tvdb_provider():
    return TVDBProvider()


def test_search_tv(tvdb_provider, mock_requests):
    """Test searching for TV shows"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": 123,
                "name": "Test Show",
                "original_name": "Original Name",
                "overview": "Test Overview",
                "firstAired": "2024-01-01",
                "language": "en",
            }
        ]
    }
    mock_requests.get.return_value = mock_response

    results = tvdb_provider.search("Test Show", year="2024", content_type="tv")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "123"
    assert results[0].title == "Test Show"
    assert results[0].original_title == "Original Name"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "en"


def test_get_by_id_tv(tvdb_provider, mock_requests):
    """Test getting TV show by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "id": 123,
            "name": "Test Show",
            "original_name": "Original Name",
            "overview": "Test Overview",
            "firstAired": "2024-01-01",
            "language": "en",
        }
    }
    mock_requests.get.return_value = mock_response

    result = tvdb_provider.get_by_id("123", content_type="tv")

    assert isinstance(result, MetadataResult)
    assert result.id == "123"
    assert result.title == "Test Show"
    assert result.original_title == "Original Name"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "en"


def test_get_external_ids(tvdb_provider, mock_requests):
    """Test getting external IDs"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"imdbId": "tt1234567", "tmdbId": "456", "tvRageId": "789"}
    }
    mock_requests.get.return_value = mock_response

    result = tvdb_provider.get_external_ids("123", content_type="tv")

    assert result == {"imdb_id": "tt1234567", "tmdb_id": "456", "tvrage_id": "789"}


def test_get_keywords(tvdb_provider, mock_requests):
    """Test getting keywords"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [{"id": 1, "name": "action"}, {"id": 2, "name": "drama"}]
    }
    mock_requests.get.return_value = mock_response

    result = tvdb_provider.get_keywords("123", content_type="tv")

    assert result == ["action", "drama"]


def test_get_trailers(tvdb_provider, mock_requests):
    """Test getting trailers"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {"id": 1, "url": "https://youtube.com/watch?v=abc123", "type": "trailer"}
        ]
    }
    mock_requests.get.return_value = mock_response

    result = tvdb_provider.get_trailers("123", content_type="tv")

    assert result == ["https://youtube.com/watch?v=abc123"]


def test_error_handling(tvdb_provider, mock_requests):
    """Test error handling"""
    mock_requests.get.side_effect = Exception("API Error")

    # Test search error
    results = tvdb_provider.search("Test")
    assert len(results) == 0

    # Test get_by_id error
    result = tvdb_provider.get_by_id("123")
    assert result is None

    # Test get_external_ids error
    result = tvdb_provider.get_external_ids("123")
    assert result == {}

    # Test get_keywords error
    result = tvdb_provider.get_keywords("123")
    assert result == []

    # Test get_trailers error
    result = tvdb_provider.get_trailers("123")
    assert result == []


def test_authentication(tvdb_provider, mock_requests):
    """Test authentication flow"""
    # Mock login response
    login_response = MagicMock()
    login_response.json.return_value = {"data": {"token": "test_token"}}

    # Mock data response
    data_response = MagicMock()
    data_response.json.return_value = {"data": {"id": 123, "name": "Test Show"}}

    # Set up mock to return different responses
    mock_requests.get.side_effect = [login_response, data_response]

    # Test that authentication is handled
    result = tvdb_provider.get_by_id("123", content_type="tv")

    assert result is not None
    assert result.id == "123"
    assert result.title == "Test Show"

    # Verify that the token was used in the second request
    assert mock_requests.get.call_count == 2
    assert "Authorization" in mock_requests.get.call_args[1]["headers"]
