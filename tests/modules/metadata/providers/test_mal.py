import pytest
from datetime import date

from modules.metadata.providers.mal import MALProvider
from modules.metadata.base import MetadataResult


@pytest.fixture
def mal_provider():
    return MALProvider()


def test_search_anime(mal_provider, mock_jikan):
    """Test searching for anime"""
    mock_jikan.search.return_value = {
        "results": [
            {
                "mal_id": 123,
                "title": "Test Anime",
                "title_english": "Test Anime",
                "title_japanese": "Original Title",
                "synopsis": "Test Overview",
                "aired": "2024-01-01",
                "type": "TV",
            }
        ]
    }

    results = mal_provider.search("Test Anime", year="2024", content_type="anime")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "123"
    assert results[0].title == "Test Anime"
    assert results[0].original_title == "Original Title"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "ja"


def test_get_by_id_anime(mal_provider, mock_jikan):
    """Test getting anime by ID"""
    mock_jikan.anime.return_value = {
        "mal_id": 123,
        "title": "Test Anime",
        "title_english": "Test Anime",
        "title_japanese": "Original Title",
        "synopsis": "Test Overview",
        "aired": "2024-01-01",
        "type": "TV",
    }

    result = mal_provider.get_by_id("123", content_type="anime")

    assert isinstance(result, MetadataResult)
    assert result.id == "123"
    assert result.title == "Test Anime"
    assert result.original_title == "Original Title"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "ja"


def test_get_external_ids(mal_provider, mock_jikan):
    """Test getting external IDs"""
    mock_jikan.anime.return_value = {
        "mal_id": 123,
        "url": "https://myanimelist.net/anime/123",
        "external_links": [
            {"name": "AniDB", "url": "https://anidb.net/anime/456"},
            {"name": "AniList", "url": "https://anilist.co/anime/789"},
            {"name": "Kitsu", "url": "https://kitsu.io/anime/101"},
        ],
    }

    result = mal_provider.get_external_ids("123", content_type="anime")

    assert result == {"anidb_id": "456", "anilist_id": "789", "kitsu_id": "101"}


def test_get_keywords(mal_provider, mock_jikan):
    """Test getting keywords"""
    mock_jikan.anime.return_value = {
        "mal_id": 123,
        "genres": [{"mal_id": 1, "name": "Action"}, {"mal_id": 2, "name": "Drama"}],
        "themes": [{"mal_id": 3, "name": "Military"}, {"mal_id": 4, "name": "School"}],
    }

    result = mal_provider.get_keywords("123", content_type="anime")

    assert result == ["Action", "Drama", "Military", "School"]


def test_get_trailers(mal_provider, mock_jikan):
    """Test getting trailers"""
    mock_jikan.anime.return_value = {
        "mal_id": 123,
        "videos": [
            {
                "title": "Trailer 1",
                "url": "https://youtube.com/watch?v=abc123",
                "type": "PV",
            }
        ],
    }

    result = mal_provider.get_trailers("123", content_type="anime")

    assert result == ["https://youtube.com/watch?v=abc123"]


def test_error_handling(mal_provider, mock_jikan):
    """Test error handling"""
    mock_jikan.search.side_effect = Exception("API Error")
    mock_jikan.anime.side_effect = Exception("API Error")

    # Test search error
    results = mal_provider.search("Test")
    assert len(results) == 0

    # Test get_by_id error
    result = mal_provider.get_by_id("123")
    assert result is None

    # Test get_external_ids error
    result = mal_provider.get_external_ids("123")
    assert result == {}

    # Test get_keywords error
    result = mal_provider.get_keywords("123")
    assert result == []

    # Test get_trailers error
    result = mal_provider.get_trailers("123")
    assert result == []


def test_content_type_filtering(mal_provider, mock_jikan):
    """Test content type filtering"""
    mock_jikan.search.return_value = {
        "results": [
            {"mal_id": 123, "title": "Test Anime", "type": "TV"},
            {"mal_id": 456, "title": "Test Manga", "type": "Manga"},
        ]
    }

    # Test anime filtering
    results = mal_provider.search("Test", content_type="anime")
    assert len(results) == 1
    assert results[0].id == "123"

    # Test manga filtering
    results = mal_provider.search("Test", content_type="manga")
    assert len(results) == 1
    assert results[0].id == "456"
