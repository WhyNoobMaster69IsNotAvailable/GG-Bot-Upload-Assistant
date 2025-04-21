import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.providers.imdb import IMDBProvider
from modules.metadata.base import MetadataResult


@pytest.fixture
def imdb_provider():
    return IMDBProvider()


def test_search_movie(imdb_provider, mock_requests):
    """Test searching for movies"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "id": "tt1234567",
                "title": "Test Movie",
                "original_title": "Original Title",
                "overview": "Test Overview",
                "release_date": "2024-01-01",
                "language": "en",
            }
        ]
    }
    mock_requests.get.return_value = mock_response

    results = imdb_provider.search("Test Movie", year="2024", content_type="movie")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "tt1234567"
    assert results[0].title == "Test Movie"
    assert results[0].original_title == "Original Title"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "en"


def test_search_tv(imdb_provider, mock_requests):
    """Test searching for TV shows"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "id": "tt7654321",
                "title": "Test Show",
                "original_title": "Original Name",
                "overview": "Test Overview",
                "release_date": "2024-01-01",
                "language": "en",
            }
        ]
    }
    mock_requests.get.return_value = mock_response

    results = imdb_provider.search("Test Show", year="2024", content_type="tv")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "tt7654321"
    assert results[0].title == "Test Show"
    assert results[0].original_title == "Original Name"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "en"


def test_get_by_id_movie(imdb_provider, mock_requests):
    """Test getting movie by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "tt1234567",
        "title": "Test Movie",
        "original_title": "Original Title",
        "overview": "Test Overview",
        "release_date": "2024-01-01",
        "language": "en",
    }
    mock_requests.get.return_value = mock_response

    result = imdb_provider.get_by_id("tt1234567", content_type="movie")

    assert isinstance(result, MetadataResult)
    assert result.id == "tt1234567"
    assert result.title == "Test Movie"
    assert result.original_title == "Original Title"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "en"


def test_get_by_id_tv(imdb_provider, mock_requests):
    """Test getting TV show by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "tt7654321",
        "title": "Test Show",
        "original_title": "Original Name",
        "overview": "Test Overview",
        "release_date": "2024-01-01",
        "language": "en",
    }
    mock_requests.get.return_value = mock_response

    result = imdb_provider.get_by_id("tt7654321", content_type="tv")

    assert isinstance(result, MetadataResult)
    assert result.id == "tt7654321"
    assert result.title == "Test Show"
    assert result.original_title == "Original Name"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "en"


def test_get_external_ids(imdb_provider, mock_requests):
    """Test getting external IDs"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tmdb_id": "123",
        "tvdb_id": "456",
        "tvrage_id": "789",
    }
    mock_requests.get.return_value = mock_response

    result = imdb_provider.get_external_ids("tt1234567", content_type="movie")

    assert result == {"tmdb_id": "123", "tvdb_id": "456", "tvrage_id": "789"}


def test_get_keywords(imdb_provider, mock_requests):
    """Test getting keywords"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "keywords": [{"id": 1, "name": "action"}, {"id": 2, "name": "drama"}]
    }
    mock_requests.get.return_value = mock_response

    result = imdb_provider.get_keywords("tt1234567", content_type="movie")

    assert result == ["action", "drama"]


def test_get_trailers(imdb_provider, mock_requests):
    """Test getting trailers"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"key": "abc123", "site": "YouTube", "type": "Trailer"}]
    }
    mock_requests.get.return_value = mock_response

    result = imdb_provider.get_trailers("tt1234567", content_type="movie")

    assert result == ["https://youtube.com/watch?v=abc123"]


def test_error_handling(imdb_provider, mock_requests):
    """Test error handling"""
    mock_requests.get.side_effect = Exception("API Error")

    # Test search error
    results = imdb_provider.search("Test")
    assert len(results) == 0

    # Test get_by_id error
    result = imdb_provider.get_by_id("tt1234567")
    assert result is None

    # Test get_external_ids error
    result = imdb_provider.get_external_ids("tt1234567")
    assert result == {}

    # Test get_keywords error
    result = imdb_provider.get_keywords("tt1234567")
    assert result == []

    # Test get_trailers error
    result = imdb_provider.get_trailers("tt1234567")
    assert result == []
