import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.providers.anidb import AniDBProvider
from modules.metadata.base import MetadataResult


@pytest.fixture
def anidb_provider():
    return AniDBProvider()


def test_search_anime(anidb_provider, mock_requests):
    """Test searching for anime"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "id": 123,
                "title": "Test Anime",
                "original_title": "Original Title",
                "overview": "Test Overview",
                "release_date": "2024-01-01",
                "language": "ja",
            }
        ]
    }
    mock_requests.get.return_value = mock_response

    results = anidb_provider.search("Test Anime", year="2024", content_type="anime")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "123"
    assert results[0].title == "Test Anime"
    assert results[0].original_title == "Original Title"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "ja"


def test_get_by_id_anime(anidb_provider, mock_requests):
    """Test getting anime by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 123,
        "title": "Test Anime",
        "original_title": "Original Title",
        "overview": "Test Overview",
        "release_date": "2024-01-01",
        "language": "ja",
    }
    mock_requests.get.return_value = mock_response

    result = anidb_provider.get_by_id("123", content_type="anime")

    assert isinstance(result, MetadataResult)
    assert result.id == "123"
    assert result.title == "Test Anime"
    assert result.original_title == "Original Title"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "ja"


def test_get_external_ids(anidb_provider, mock_requests):
    """Test getting external IDs"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "mal_id": "456",
        "anilist_id": "789",
        "kitsu_id": "101",
    }
    mock_requests.get.return_value = mock_response

    result = anidb_provider.get_external_ids("123", content_type="anime")

    assert result == {"mal_id": "456", "anilist_id": "789", "kitsu_id": "101"}


def test_get_keywords(anidb_provider, mock_requests):
    """Test getting keywords"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tags": [{"id": 1, "name": "action"}, {"id": 2, "name": "drama"}]
    }
    mock_requests.get.return_value = mock_response

    result = anidb_provider.get_keywords("123", content_type="anime")

    assert result == ["action", "drama"]


def test_get_trailers(anidb_provider, mock_requests):
    """Test getting trailers"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "videos": [
            {"id": 1, "url": "https://youtube.com/watch?v=abc123", "type": "trailer"}
        ]
    }
    mock_requests.get.return_value = mock_response

    result = anidb_provider.get_trailers("123", content_type="anime")

    assert result == ["https://youtube.com/watch?v=abc123"]


def test_error_handling(anidb_provider, mock_requests):
    """Test error handling"""
    mock_requests.get.side_effect = Exception("API Error")

    # Test search error
    results = anidb_provider.search("Test")
    assert len(results) == 0

    # Test get_by_id error
    result = anidb_provider.get_by_id("123")
    assert result is None

    # Test get_external_ids error
    result = anidb_provider.get_external_ids("123")
    assert result == {}

    # Test get_keywords error
    result = anidb_provider.get_keywords("123")
    assert result == []

    # Test get_trailers error
    result = anidb_provider.get_trailers("123")
    assert result == []


def test_authentication(anidb_provider, mock_requests):
    """Test authentication flow"""
    # Mock login response
    login_response = MagicMock()
    login_response.json.return_value = {"token": "test_token"}

    # Mock data response
    data_response = MagicMock()
    data_response.json.return_value = {"id": 123, "title": "Test Anime"}

    # Set up mock to return different responses
    mock_requests.get.side_effect = [login_response, data_response]

    # Test that authentication is handled
    result = anidb_provider.get_by_id("123", content_type="anime")

    assert result is not None
    assert result.id == "123"
    assert result.title == "Test Anime"

    # Verify that the token was used in the second request
    assert mock_requests.get.call_count == 2
    assert "Authorization" in mock_requests.get.call_args[1]["headers"]
