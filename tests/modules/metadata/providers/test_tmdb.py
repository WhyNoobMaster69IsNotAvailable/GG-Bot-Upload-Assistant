import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.providers.tmdb import TMDBProvider
from modules.metadata.base import MetadataResult


@pytest.fixture
def tmdb_provider():
    return TMDBProvider()


def test_search_movie(tmdb_provider, mock_requests):
    """Test searching for movies"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "id": 123,
                "title": "Test Movie",
                "original_title": "Original Title",
                "overview": "Test Overview",
                "release_date": "2024-01-01",
                "original_language": "en",
            }
        ]
    }
    mock_requests.get.return_value = mock_response

    results = tmdb_provider.search("Test Movie", year="2024", content_type="movie")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "123"
    assert results[0].title == "Test Movie"
    assert results[0].original_title == "Original Title"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "en"


def test_search_tv(tmdb_provider, mock_requests):
    """Test searching for TV shows"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "id": 456,
                "name": "Test Show",
                "original_name": "Original Name",
                "overview": "Test Overview",
                "first_air_date": "2024-01-01",
                "original_language": "en",
            }
        ]
    }
    mock_requests.get.return_value = mock_response

    results = tmdb_provider.search("Test Show", year="2024", content_type="tv")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "456"
    assert results[0].title == "Test Show"
    assert results[0].original_title == "Original Name"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "en"


def test_get_by_id_movie(tmdb_provider, mock_requests):
    """Test getting movie by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 123,
        "title": "Test Movie",
        "original_title": "Original Title",
        "overview": "Test Overview",
        "release_date": "2024-01-01",
        "original_language": "en",
    }
    mock_requests.get.return_value = mock_response

    result = tmdb_provider.get_by_id("123", content_type="movie")

    assert isinstance(result, MetadataResult)
    assert result.id == "123"
    assert result.title == "Test Movie"
    assert result.original_title == "Original Title"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "en"


def test_get_by_id_tv(tmdb_provider, mock_requests):
    """Test getting TV show by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 456,
        "name": "Test Show",
        "original_name": "Original Name",
        "overview": "Test Overview",
        "first_air_date": "2024-01-01",
        "original_language": "en",
    }
    mock_requests.get.return_value = mock_response

    result = tmdb_provider.get_by_id("456", content_type="tv")

    assert isinstance(result, MetadataResult)
    assert result.id == "456"
    assert result.title == "Test Show"
    assert result.original_title == "Original Name"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "en"


def test_get_external_ids(tmdb_provider, mock_requests):
    """Test getting external IDs"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "imdb_id": "tt1234567",
        "tvdb_id": "123456",
        "tvrage_id": "12345",
    }
    mock_requests.get.return_value = mock_response

    result = tmdb_provider.get_external_ids("123", content_type="movie")

    assert result == {"imdb_id": "tt1234567", "tvdb_id": "123456", "tvrage_id": "12345"}


def test_get_keywords(tmdb_provider, mock_requests):
    """Test getting keywords"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "keywords": [{"id": 1, "name": "action"}, {"id": 2, "name": "drama"}]
    }
    mock_requests.get.return_value = mock_response

    result = tmdb_provider.get_keywords("123", content_type="movie")

    assert result == ["action", "drama"]


def test_get_trailers(tmdb_provider, mock_requests):
    """Test getting trailers"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"key": "abc123", "site": "YouTube", "type": "Trailer"}]
    }
    mock_requests.get.return_value = mock_response

    result = tmdb_provider.get_trailers("123", content_type="movie")

    assert result == ["https://youtube.com/watch?v=abc123"]


def test_error_handling(tmdb_provider, mock_requests):
    """Test error handling"""
    mock_requests.get.side_effect = Exception("API Error")

    # Test search error
    results = tmdb_provider.search("Test")
    assert len(results) == 0

    # Test get_by_id error
    result = tmdb_provider.get_by_id("123")
    assert result is None

    # Test get_external_ids error
    result = tmdb_provider.get_external_ids("123")
    assert result == {}

    # Test get_keywords error
    result = tmdb_provider.get_keywords("123")
    assert result == []

    # Test get_trailers error
    result = tmdb_provider.get_trailers("123")
    assert result == []
