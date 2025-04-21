import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.providers.tvmaze import TVMazeProvider
from modules.metadata.base import MetadataResult


@pytest.fixture
def tvmaze_provider():
    return TVMazeProvider()


def test_search_tv(tvmaze_provider, mock_requests):
    """Test searching for TV shows"""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": 123,
            "name": "Test Show",
            "original_name": "Original Name",
            "summary": "Test Overview",
            "premiered": "2024-01-01",
            "language": "en",
        }
    ]
    mock_requests.get.return_value = mock_response

    results = tvmaze_provider.search("Test Show", year="2024", content_type="tv")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "123"
    assert results[0].title == "Test Show"
    assert results[0].original_title == "Original Name"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "en"


def test_get_by_id_tv(tvmaze_provider, mock_requests):
    """Test getting TV show by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 123,
        "name": "Test Show",
        "original_name": "Original Name",
        "summary": "Test Overview",
        "premiered": "2024-01-01",
        "language": "en",
    }
    mock_requests.get.return_value = mock_response

    result = tvmaze_provider.get_by_id("123", content_type="tv")

    assert isinstance(result, MetadataResult)
    assert result.id == "123"
    assert result.title == "Test Show"
    assert result.original_title == "Original Name"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "en"


def test_get_external_ids(tvmaze_provider, mock_requests):
    """Test getting external IDs"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "externals": {"imdb": "tt1234567", "thetvdb": "456", "tvrage": "789"}
    }
    mock_requests.get.return_value = mock_response

    result = tvmaze_provider.get_external_ids("123", content_type="tv")

    assert result == {"imdb_id": "tt1234567", "tvdb_id": "456", "tvrage_id": "789"}


def test_get_keywords(tvmaze_provider, mock_requests):
    """Test getting keywords"""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "name": "action"},
        {"id": 2, "name": "drama"},
    ]
    mock_requests.get.return_value = mock_response

    result = tvmaze_provider.get_keywords("123", content_type="tv")

    assert result == ["action", "drama"]


def test_get_trailers(tvmaze_provider, mock_requests):
    """Test getting trailers"""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "url": "https://youtube.com/watch?v=abc123", "type": "trailer"}
    ]
    mock_requests.get.return_value = mock_response

    result = tvmaze_provider.get_trailers("123", content_type="tv")

    assert result == ["https://youtube.com/watch?v=abc123"]


def test_error_handling(tvmaze_provider, mock_requests):
    """Test error handling"""
    mock_requests.get.side_effect = Exception("API Error")

    # Test search error
    results = tvmaze_provider.search("Test")
    assert len(results) == 0

    # Test get_by_id error
    result = tvmaze_provider.get_by_id("123")
    assert result is None

    # Test get_external_ids error
    result = tvmaze_provider.get_external_ids("123")
    assert result == {}

    # Test get_keywords error
    result = tvmaze_provider.get_keywords("123")
    assert result == []

    # Test get_trailers error
    result = tvmaze_provider.get_trailers("123")
    assert result == []


def test_embedding(tvmaze_provider, mock_requests):
    """Test embedding related data"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 123,
        "name": "Test Show",
        "_embedded": {
            "cast": [
                {
                    "person": {"id": 1, "name": "Actor 1"},
                    "character": {"id": 1, "name": "Character 1"},
                }
            ],
            "crew": [{"person": {"id": 2, "name": "Crew 1"}, "type": "Director"}],
        },
    }
    mock_requests.get.return_value = mock_response

    result = tvmaze_provider.get_by_id("123", content_type="tv")

    assert result is not None
    assert result.id == "123"
    assert result.title == "Test Show"

    # Verify that the embed parameter was used in the request
    assert "embed" in mock_requests.get.call_args[1]["params"]
    assert "cast" in mock_requests.get.call_args[1]["params"]["embed"]
    assert "crew" in mock_requests.get.call_args[1]["params"]["embed"]
