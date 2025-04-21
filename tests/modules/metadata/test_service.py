import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.manager import MetadataService
from modules.metadata.base import MetadataResult, MetadataProvider


@pytest.fixture
def mock_providers():
    """Create mock providers for testing"""
    providers = {}

    # TMDB provider
    tmdb = MagicMock(spec=MetadataProvider)
    tmdb.search.return_value = [
        MetadataResult(
            id="123",
            title="Test Movie",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="en",
        )
    ]
    providers["tmdb"] = tmdb

    # IMDB provider
    imdb = MagicMock(spec=MetadataProvider)
    imdb.search.return_value = [
        MetadataResult(
            id="tt1234567",
            title="Test Movie",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="en",
        )
    ]
    providers["imdb"] = imdb

    # TVDB provider
    tvdb = MagicMock(spec=MetadataProvider)
    tvdb.search.return_value = [
        MetadataResult(
            id="456",
            title="Test Show",
            original_title="Original Name",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="en",
        )
    ]
    providers["tvdb"] = tvdb

    # AniDB provider
    anidb = MagicMock(spec=MetadataProvider)
    anidb.search.return_value = [
        MetadataResult(
            id="789",
            title="Test Anime",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="ja",
        )
    ]
    providers["anidb"] = anidb

    # TVMaze provider
    tvmaze = MagicMock(spec=MetadataProvider)
    tvmaze.search.return_value = [
        MetadataResult(
            id="101",
            title="Test Show",
            original_title="Original Name",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="en",
        )
    ]
    providers["tvmaze"] = tvmaze

    # MAL provider
    mal = MagicMock(spec=MetadataProvider)
    mal.search.return_value = [
        MetadataResult(
            id="202",
            title="Test Anime",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="ja",
        )
    ]
    providers["mal"] = mal

    # AniList provider
    anilist = MagicMock(spec=MetadataProvider)
    anilist.search.return_value = [
        MetadataResult(
            id="303",
            title="Test Anime",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="ja",
        )
    ]
    providers["anilist"] = anilist

    return providers


@pytest.fixture
def metadata_service(mock_providers):
    """Create a metadata service with mock providers"""
    service = MetadataService()
    for name, provider in mock_providers.items():
        service.register_provider(name, provider)
    return service


def test_search_movies(metadata_service, mock_providers):
    """Test searching for movies"""
    results = metadata_service.search("Test Movie", year="2024", content_type="movie")

    # Verify results
    assert len(results) == 2
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Movie" for r in results)

    # Verify that results are sorted by relevance
    assert results[0].id in ["123", "tt1234567"]
    assert results[1].id in ["123", "tt1234567"]
    assert results[0].id != results[1].id


def test_search_tv(metadata_service, mock_providers):
    """Test searching for TV shows"""
    results = metadata_service.search("Test Show", year="2024", content_type="tv")

    # Verify results
    assert len(results) == 4
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Show" for r in results)

    # Verify that results are sorted by relevance
    assert len(set(r.id for r in results)) == 4


def test_search_anime(metadata_service, mock_providers):
    """Test searching for anime"""
    results = metadata_service.search("Test Anime", year="2024", content_type="anime")

    # Verify results
    assert len(results) == 3
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Anime" for r in results)

    # Verify that results are sorted by relevance
    assert len(set(r.id for r in results)) == 3


def test_get_metadata(metadata_service, mock_providers):
    """Test getting metadata from specific providers"""
    # Test TMDB
    result = metadata_service.get_metadata("123", "tmdb")
    assert result is not None
    assert result.id == "123"
    assert result.title == "Test Movie"

    # Test IMDB
    result = metadata_service.get_metadata("tt1234567", "imdb")
    assert result is not None
    assert result.id == "tt1234567"
    assert result.title == "Test Movie"

    # Test non-existent provider
    result = metadata_service.get_metadata("123", "nonexistent")
    assert result is None


def test_get_external_ids(metadata_service, mock_providers):
    """Test getting external IDs"""
    # Set up mock responses
    mock_providers["tmdb"].get_external_ids.return_value = {
        "imdb_id": "tt1234567",
        "tvdb_id": "456",
    }
    mock_providers["imdb"].get_external_ids.return_value = {
        "tmdb_id": "123",
        "tvdb_id": "456",
    }

    # Test getting external IDs
    result = metadata_service.get_external_ids("123", "tmdb")
    assert result == {"imdb_id": "tt1234567", "tvdb_id": "456"}

    # Test non-existent provider
    result = metadata_service.get_external_ids("123", "nonexistent")
    assert result == {}


def test_get_keywords(metadata_service, mock_providers):
    """Test getting keywords"""
    # Set up mock responses
    mock_providers["tmdb"].get_keywords.return_value = ["action", "drama"]
    mock_providers["imdb"].get_keywords.return_value = ["thriller", "drama"]

    # Test getting keywords
    result = metadata_service.get_keywords("123", "tmdb")
    assert result == ["action", "drama"]

    # Test non-existent provider
    result = metadata_service.get_keywords("123", "nonexistent")
    assert result == []


def test_get_trailers(metadata_service, mock_providers):
    """Test getting trailers"""
    # Set up mock responses
    mock_providers["tmdb"].get_trailers.return_value = [
        "https://youtube.com/watch?v=abc123"
    ]
    mock_providers["imdb"].get_trailers.return_value = [
        "https://youtube.com/watch?v=def456"
    ]

    # Test getting trailers
    result = metadata_service.get_trailers("123", "tmdb")
    assert result == ["https://youtube.com/watch?v=abc123"]

    # Test non-existent provider
    result = metadata_service.get_trailers("123", "nonexistent")
    assert result == []


def test_error_handling(metadata_service, mock_providers):
    """Test error handling"""
    # Test provider error
    mock_providers["tmdb"].search.side_effect = Exception("API Error")
    results = metadata_service.search("Test", provider="tmdb")
    assert len(results) == 0

    # Test non-existent provider
    results = metadata_service.search("Test", provider="nonexistent")
    assert len(results) == 0

    # Test get_metadata error
    mock_providers["tmdb"].get_by_id.side_effect = Exception("API Error")
    result = metadata_service.get_metadata("123", "tmdb")
    assert result is None

    # Test get_external_ids error
    mock_providers["tmdb"].get_external_ids.side_effect = Exception("API Error")
    result = metadata_service.get_external_ids("123", "tmdb")
    assert result == {}


def test_provider_priority(metadata_service, mock_providers):
    """Test provider priority in search results"""
    # Set up different titles for different providers
    mock_providers["tmdb"].search.return_value = [
        MetadataResult(
            id="123",
            title="Test Movie (TMDB)",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="en",
        )
    ]
    mock_providers["imdb"].search.return_value = [
        MetadataResult(
            id="tt1234567",
            title="Test Movie (IMDB)",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="en",
        )
    ]

    # Test that results are ordered by provider priority
    results = metadata_service.search("Test Movie", year="2024", content_type="movie")
    assert len(results) == 2
    assert results[0].title == "Test Movie (TMDB)"  # TMDB should be first
    assert results[1].title == "Test Movie (IMDB)"  # IMDB should be second
