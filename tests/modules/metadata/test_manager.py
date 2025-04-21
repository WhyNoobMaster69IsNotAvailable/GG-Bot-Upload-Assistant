import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.manager import MetadataManager
from modules.metadata.base import MetadataResult, MetadataProvider, parse_date_string


def test_date_parsing():
    """Test parsing of various date string formats"""
    # Test date with country
    assert parse_date_string("18 Jul 2008 (India)") == date(2008, 7, 18)

    # Test simple date
    assert parse_date_string("18 Jul 2008") == date(2008, 7, 18)

    # Test various date formats
    assert parse_date_string("2008-07-18") == date(2008, 7, 18)
    assert parse_date_string("July 18, 2008") == date(2008, 7, 18)
    assert parse_date_string("18/07/2008") == date(2008, 7, 18)

    # Test invalid dates
    assert parse_date_string("Invalid Date") is None
    assert parse_date_string("") is None
    assert parse_date_string(None) is None


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

    # IMDB provider with string date
    imdb = MagicMock(spec=MetadataProvider)
    imdb.search.return_value = [
        MetadataResult(
            id="tt1234567",
            title="Test Movie",
            original_title="Original Title",
            overview="Test Overview",
            release_date="18 Jul 2008 (India)",
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
            original_title="アニメタイトル",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="ja",
            keywords=["anime", "manga"],
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
            original_title="アニメタイトル",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="ja",
            keywords=["anime", "manga"],
        )
    ]
    providers["mal"] = mal

    # AniList provider
    anilist = MagicMock(spec=MetadataProvider)
    anilist.search.return_value = [
        MetadataResult(
            id="303",
            title="Test Anime",
            original_title="アニメタイトル",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="ja",
            keywords=["anime", "manga"],
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


def test_search_movies(metadata_manager, mock_providers):
    """Test searching for movies"""
    results = metadata_manager.search("Test Movie", year="2024", content_type="movie")

    # Verify that only movie providers were called
    assert mock_providers["tmdb"].search.called
    assert mock_providers["imdb"].search.called
    assert not mock_providers["tvdb"].search.called
    assert not mock_providers["tvmaze"].search.called
    assert not mock_providers["anidb"].search.called
    assert not mock_providers["mal"].search.called
    assert not mock_providers["anilist"].search.called

    # Verify results
    assert len(results) == 2
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Movie" for r in results)
    # Verify provider field is set
    assert any(r.provider == "tmdb" for r in results)
    assert any(r.provider == "imdb" for r in results)


def test_search_tv(metadata_manager, mock_providers):
    """Test searching for TV shows"""
    # FAILED
    results = metadata_manager.search("Test Show", year="2024", content_type="episode")

    # Verify that TV providers were called
    assert mock_providers["tmdb"].search.called
    assert mock_providers["imdb"].search.called
    assert mock_providers["tvdb"].search.called
    assert mock_providers["tvmaze"].search.called
    assert not mock_providers["anidb"].search.called
    assert not mock_providers["mal"].search.called
    assert not mock_providers["anilist"].search.called

    # Verify results
    assert len(results) == 4
    assert all(isinstance(r, MetadataResult) for r in results)
    assert all(r.title == "Test Show" for r in results)
    # Verify provider field is set
    assert any(r.provider == "tmdb" for r in results)
    assert any(r.provider == "imdb" for r in results)
    assert any(r.provider == "tvdb" for r in results)
    assert any(r.provider == "tvmaze" for r in results)


def test_search_tv_with_anime_detection(metadata_manager, mock_providers):
    """Test searching for TV shows that are detected as anime"""
    # Modify TVDB result to look like anime
    mock_providers["tvdb"].search.return_value = [
        MetadataResult(
            id="456",
            title="Test Anime Show",
            original_title="アニメタイトル",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="ja",
            keywords=["anime", "manga"],
        )
    ]

    results = metadata_manager.search(
        "Test Anime Show", year="2024", content_type="episode"
    )

    # Verify that both TV and anime providers were called
    assert mock_providers["tmdb"].search.called
    assert mock_providers["imdb"].search.called
    assert mock_providers["tvdb"].search.called
    assert mock_providers["tvmaze"].search.called
    assert mock_providers["anidb"].search.called
    assert mock_providers["mal"].search.called
    assert mock_providers["anilist"].search.called

    # Verify results
    assert len(results) > 4  # Should have results from both TV and anime providers
    assert any(r.language == "ja" for r in results)
    # Verify provider field is set for both TV and anime results
    assert any(r.provider == "tvdb" for r in results)
    assert any(r.provider in ["anidb", "mal", "anilist"] for r in results)


def test_search_tv_no_results_then_anime(metadata_manager, mock_providers):
    """Test searching for TV shows with no results, then trying anime providers"""
    # Make TV providers return no results
    mock_providers["tmdb"].search.return_value = []
    mock_providers["imdb"].search.return_value = []
    mock_providers["tvdb"].search.return_value = []
    mock_providers["tvmaze"].search.return_value = []

    results = metadata_manager.search("Test Show", year="2024", content_type="episode")

    # Verify that all providers were called
    assert mock_providers["tmdb"].search.called
    assert mock_providers["imdb"].search.called
    assert mock_providers["tvdb"].search.called
    assert mock_providers["tvmaze"].search.called
    assert mock_providers["anidb"].search.called
    assert mock_providers["mal"].search.called
    assert mock_providers["anilist"].search.called

    # Verify results
    assert len(results) == 3  # Should have results from anime providers
    assert all(r.language == "ja" for r in results)
    # Verify provider field is set for anime results
    assert any(r.provider == "anidb" for r in results)
    assert any(r.provider == "mal" for r in results)
    assert any(r.provider == "anilist" for r in results)


def test_invalid_content_type(metadata_manager, mock_providers):
    """Test searching with invalid content type"""
    results = metadata_manager.search("Test", year="2024", content_type="invalid")

    # Verify that no providers were called
    assert not mock_providers["tmdb"].search.called
    assert not mock_providers["imdb"].search.called
    assert not mock_providers["tvdb"].search.called
    assert not mock_providers["tvmaze"].search.called
    assert not mock_providers["anidb"].search.called
    assert not mock_providers["mal"].search.called
    assert not mock_providers["anilist"].search.called

    # Verify empty results
    assert len(results) == 0


def test_error_handling(metadata_manager, mock_providers):
    """Test error handling in the manager"""
    # FAILED
    # Test provider error
    mock_providers["tmdb"].search.side_effect = Exception("API Error")
    results = metadata_manager.search("Test", content_type="movie")
    assert len(results) == 1  # Should still get results from IMDB

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


def test_metadata_result_date_parsing():
    """Test that MetadataResult automatically parses date strings"""
    # Test with date string containing country
    result = MetadataResult(id="1", title="Test", release_date="18 Jul 2008 (India)")
    assert result.release_date == date(2008, 7, 18)

    # Test with simple date string
    result = MetadataResult(id="1", title="Test", release_date="18 Jul 2008")
    assert result.release_date == date(2008, 7, 18)

    # Test with date object
    result = MetadataResult(id="1", title="Test", release_date=date(2008, 7, 18))
    assert result.release_date == date(2008, 7, 18)

    # Test with invalid date
    result = MetadataResult(id="1", title="Test", release_date="Invalid Date")
    assert result.release_date is None
