import pytest
from datetime import date
from unittest.mock import MagicMock

from modules.metadata.providers.anilist import AniListProvider
from modules.metadata.base import MetadataResult


@pytest.fixture
def anilist_provider():
    return AniListProvider()


def test_search_anime(anilist_provider, mock_requests):
    """Test searching for anime"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "Page": {
                "media": [
                    {
                        "id": 123,
                        "title": {
                            "romaji": "Test Anime",
                            "english": "Test Anime",
                            "native": "Original Title",
                        },
                        "description": "Test Overview",
                        "startDate": {"year": 2024, "month": 1, "day": 1},
                        "type": "ANIME",
                    }
                ]
            }
        }
    }
    mock_requests.post.return_value = mock_response

    results = anilist_provider.search("Test Anime", year="2024", content_type="anime")

    assert len(results) == 1
    assert isinstance(results[0], MetadataResult)
    assert results[0].id == "123"
    assert results[0].title == "Test Anime"
    assert results[0].original_title == "Original Title"
    assert results[0].overview == "Test Overview"
    assert results[0].release_date == date(2024, 1, 1)
    assert results[0].language == "ja"


def test_get_by_id_anime(anilist_provider, mock_requests):
    """Test getting anime by ID"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "Media": {
                "id": 123,
                "title": {
                    "romaji": "Test Anime",
                    "english": "Test Anime",
                    "native": "Original Title",
                },
                "description": "Test Overview",
                "startDate": {"year": 2024, "month": 1, "day": 1},
                "type": "ANIME",
            }
        }
    }
    mock_requests.post.return_value = mock_response

    result = anilist_provider.get_by_id("123", content_type="anime")

    assert isinstance(result, MetadataResult)
    assert result.id == "123"
    assert result.title == "Test Anime"
    assert result.original_title == "Original Title"
    assert result.overview == "Test Overview"
    assert result.release_date == date(2024, 1, 1)
    assert result.language == "ja"


def test_get_external_ids(anilist_provider, mock_requests):
    """Test getting external IDs"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "Media": {"id": 123, "idMal": "456", "idAniDB": "789", "idKitsu": "101"}
        }
    }
    mock_requests.post.return_value = mock_response

    result = anilist_provider.get_external_ids("123", content_type="anime")

    assert result == {"mal_id": "456", "anidb_id": "789", "kitsu_id": "101"}


def test_get_keywords(anilist_provider, mock_requests):
    """Test getting keywords"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "Media": {
                "id": 123,
                "genres": ["Action", "Drama"],
                "tags": [{"name": "Military"}, {"name": "School"}],
            }
        }
    }
    mock_requests.post.return_value = mock_response

    result = anilist_provider.get_keywords("123", content_type="anime")

    assert result == ["Action", "Drama", "Military", "School"]


def test_get_trailers(anilist_provider, mock_requests):
    """Test getting trailers"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"Media": {"id": 123, "trailer": {"id": "abc123", "site": "youtube"}}}
    }
    mock_requests.post.return_value = mock_response

    result = anilist_provider.get_trailers("123", content_type="anime")

    assert result == ["https://youtube.com/watch?v=abc123"]


def test_error_handling(anilist_provider, mock_requests):
    """Test error handling"""
    mock_requests.post.side_effect = Exception("API Error")

    # Test search error
    results = anilist_provider.search("Test")
    assert len(results) == 0

    # Test get_by_id error
    result = anilist_provider.get_by_id("123")
    assert result is None

    # Test get_external_ids error
    result = anilist_provider.get_external_ids("123")
    assert result == {}

    # Test get_keywords error
    result = anilist_provider.get_keywords("123")
    assert result == []

    # Test get_trailers error
    result = anilist_provider.get_trailers("123")
    assert result == []


def test_authentication(anilist_provider, mock_requests):
    """Test authentication flow"""
    # Mock token response
    token_response = MagicMock()
    token_response.json.return_value = {"access_token": "test_token"}

    # Mock data response
    data_response = MagicMock()
    data_response.json.return_value = {
        "data": {"Media": {"id": 123, "title": {"romaji": "Test Anime"}}}
    }

    # Set up mock to return different responses
    mock_requests.post.side_effect = [token_response, data_response]

    # Test that authentication is handled
    result = anilist_provider.get_by_id("123", content_type="anime")

    assert result is not None
    assert result.id == "123"
    assert result.title == "Test Anime"

    # Verify that the token was used in the second request
    assert mock_requests.post.call_count == 2
    assert "Authorization" in mock_requests.post.call_args[1]["headers"]


def test_graphql_queries(anilist_provider, mock_requests):
    """Test GraphQL query construction"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"Media": {"id": 123, "title": {"romaji": "Test Anime"}}}
    }
    mock_requests.post.return_value = mock_response

    # Test search query
    anilist_provider.search("Test")
    search_query = mock_requests.post.call_args[1]["json"]["query"]
    assert "query" in search_query
    assert "Page" in search_query
    assert "media" in search_query

    # Test get_by_id query
    anilist_provider.get_by_id("123")
    get_query = mock_requests.post.call_args[1]["json"]["query"]
    assert "query" in get_query
    assert "Media" in get_query
    assert "id" in get_query
