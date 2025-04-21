import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.manager import MetadataManager
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
def metadata_manager(mock_providers):
    """Create a metadata manager with mock providers"""
    manager = MetadataManager()
    for name, provider in mock_providers.items():
        manager.register_provider(name, provider)
    return manager


def test_provider_registration(metadata_manager, mock_providers):
    """Test provider registration"""
    # Test that all providers are registered
    for name, provider in mock_providers.items():
        assert name in metadata_manager.providers
        assert metadata_manager.providers[name] == provider

    # Test overwriting a provider
    new_provider = MagicMock(spec=MetadataProvider)
    metadata_manager.register_provider("tmdb", new_provider)
    assert metadata_manager.providers["tmdb"] == new_provider


def test_search_movies(metadata_manager, mock_providers):
    """Test searching for movies across providers"""
    results = metadata_manager.search("Test Movie", year="2024", content_type="movie")

    # Verify that all relevant providers were called
    assert mock_providers["tmdb"].search.called
    assert mock_providers["imdb"].search.called

    # Verify that TV-focused providers were not called
    assert not mock_providers["tvdb"].search.called
    assert not mock_providers["tvmaze"].search.called

    # Verify that anime providers were not called
    assert not mock_providers["anidb"].search.called
    assert not mock_providers["mal"].search.called
    assert not mock_providers["anilist"].search.called

    # Verify results
    assert len(results) == 2
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Movie" for r in results)


def test_search_tv(metadata_manager, mock_providers):
    """Test searching for TV shows across providers"""
    results = metadata_manager.search("Test Show", year="2024", content_type="tv")

    # Verify that all relevant providers were called
    assert mock_providers["tmdb"].search.called
    assert mock_providers["imdb"].search.called
    assert mock_providers["tvdb"].search.called
    assert mock_providers["tvmaze"].search.called

    # Verify that anime providers were not called
    assert not mock_providers["anidb"].search.called
    assert not mock_providers["mal"].search.called
    assert not mock_providers["anilist"].search.called

    # Verify results
    assert len(results) == 4
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Show" for r in results)


def test_search_anime(metadata_manager, mock_providers):
    """Test searching for anime across providers"""
    results = metadata_manager.search("Test Anime", year="2024", content_type="anime")

    # Verify that all relevant providers were called
    assert mock_providers["anidb"].search.called
    assert mock_providers["mal"].search.called
    assert mock_providers["anilist"].search.called

    # Verify that other providers were not called
    assert not mock_providers["tmdb"].search.called
    assert not mock_providers["imdb"].search.called
    assert not mock_providers["tvdb"].search.called
    assert not mock_providers["tvmaze"].search.called

    # Verify results
    assert len(results) == 3
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Anime" for r in results)


def test_get_metadata(metadata_manager, mock_providers):
    """Test getting metadata from specific providers"""
    # Test TMDB
    result = metadata_manager.get_metadata("123", "tmdb")
    assert mock_providers["tmdb"].get_by_id.called
    assert result is not None
    assert result.id == "123"

    # Test IMDB
    result = metadata_manager.get_metadata("tt1234567", "imdb")
    assert mock_providers["imdb"].get_by_id.called
    assert result is not None
    assert result.id == "tt1234567"

    # Test non-existent provider
    result = metadata_manager.get_metadata("123", "nonexistent")
    assert result is None


def test_get_external_ids(metadata_manager, mock_providers):
    """Test getting external IDs from providers"""
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
    result = metadata_manager.get_external_ids("123", "tmdb")
    assert result == {"imdb_id": "tt1234567", "tvdb_id": "456"}

    # Test non-existent provider
    result = metadata_manager.get_external_ids("123", "nonexistent")
    assert result == {}


def test_error_handling(metadata_manager, mock_providers):
    """Test error handling in the manager"""
    # Test provider error
    mock_providers["tmdb"].search.side_effect = Exception("API Error")
    results = metadata_manager.search("Test", provider="tmdb")
    assert len(results) == 0

    # Test non-existent provider
    results = metadata_manager.search("Test", provider="nonexistent")
    assert len(results) == 0

    # Test get_metadata error
    mock_providers["tmdb"].get_by_id.side_effect = Exception("API Error")
    result = metadata_manager.get_metadata("123", "tmdb")
    assert result is None

    # Test get_external_ids error
    mock_providers["tmdb"].get_external_ids.side_effect = Exception("API Error")
    result = metadata_manager.get_external_ids("123", "tmdb")
    assert result == {}
