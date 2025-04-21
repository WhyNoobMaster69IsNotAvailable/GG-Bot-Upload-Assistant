from datetime import date
from typing import Dict, List

from modules.metadata.base import MetadataResult, MetadataProvider, MetadataManager
from modules.metadata.providers.imdb import IMDBProvider


class TestMetadataBase:
    def test_metadata_result_creation(self):
        """Test creating a MetadataResult instance"""
        result = MetadataResult(
            id="123",
            title="Test Title",
            original_title="Original Title",
            overview="Test Overview",
            release_date=date(2024, 1, 1),
            language="en",
            external_ids={"imdb_id": "tt1234567"},
            keywords=["action", "drama"],
            trailers=["https://youtube.com/watch?v=abc123"],
        )

        assert result.id == "123"
        assert result.title == "Test Title"
        assert result.original_title == "Original Title"
        assert result.overview == "Test Overview"
        assert result.release_date == date(2024, 1, 1)
        assert result.language == "en"
        assert result.external_ids == {"imdb_id": "tt1234567"}
        assert result.keywords == ["action", "drama"]
        assert result.trailers == ["https://youtube.com/watch?v=abc123"]

    def test_metadata_result_optional_fields(self):
        """Test creating a MetadataResult with optional fields"""
        result = MetadataResult(id="123", title="Test Title")

        assert result.id == "123"
        assert result.title == "Test Title"
        assert result.original_title is None
        assert result.overview is None
        assert result.release_date is None
        assert result.language is None
        assert result.external_ids is None
        assert result.keywords is None
        assert result.trailers is None

    def test_metadata_provider_abstract_methods(self):
        """Test that MetadataProvider is abstract and requires implementation of methods"""

        class TestProvider(MetadataProvider):
            def search(
                self, query: str, year: str = None, content_type: str = "movie"
            ) -> List[MetadataResult]:
                return []

            def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
                return None

            def get_external_ids(
                self, id: str, content_type: str = "movie"
            ) -> Dict[str, str]:
                return {}

            def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
                return []

            def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
                return []

        # Should not raise any errors
        provider = TestProvider()

        # Test that abstract methods are called
        assert provider.search("test") == []
        assert provider.get_by_id("123") is None
        assert provider.get_external_ids("123") == {}
        assert provider.get_keywords("123") == []
        assert provider.get_trailers("123") == []

    def test_metadata_manager_registration(
        self, metadata_manager: MetadataManager, mock_provider: MetadataProvider
    ):
        """Test provider registration in MetadataManager"""
        # Test registering a new provider
        metadata_manager.register_provider("test", mock_provider)
        assert "test" in metadata_manager.providers
        assert metadata_manager.providers["test"] == mock_provider

        # Test overwriting an existing provider
        new_provider = IMDBProvider()
        metadata_manager.register_provider("test", new_provider)
        assert metadata_manager.providers["test"] == new_provider

    def test_metadata_manager_search(
        self,
        metadata_manager: MetadataManager,
        mock_provider: MetadataProvider,
        mock_metadata_result: MetadataResult,
    ):
        """Test search functionality in MetadataManager"""
        # FAILED
        mock_provider.search.return_value = [mock_metadata_result]

        results = metadata_manager.search("test")
        assert len(results) == 1
        assert results[0] == mock_metadata_result

        # Test error handling
        mock_provider.search.side_effect = Exception("Test error")
        results = metadata_manager.search("test")
        assert len(results) == 0

    def test_metadata_manager_get_metadata(
        self,
        metadata_manager: MetadataManager,
        mock_provider: MetadataProvider,
        mock_metadata_result: MetadataResult,
    ):
        """Test get_metadata functionality in MetadataManager"""
        mock_provider.get_by_id.return_value = mock_metadata_result

        result = metadata_manager.get_metadata("123", "mock")
        assert result == mock_metadata_result

        # Test non-existent provider
        result = metadata_manager.get_metadata("123", "nonexistent")
        assert result is None

        # Test error handling
        mock_provider.get_by_id.side_effect = Exception("Test error")
        result = metadata_manager.get_metadata("123", "mock")
        assert result is None

    def test_metadata_manager_get_external_ids(
        self, metadata_manager: MetadataManager, mock_provider: MetadataProvider
    ):
        """Test get_external_ids functionality in MetadataManager"""
        mock_provider.get_external_ids.return_value = {"imdb_id": "tt1234567"}

        result = metadata_manager.get_external_ids("123", "mock")
        assert result == {"imdb_id": "tt1234567"}

        # Test non-existent provider
        result = metadata_manager.get_external_ids("123", "nonexistent")
        assert result == {}

        # Test error handling
        mock_provider.get_external_ids.side_effect = Exception("Test error")
        result = metadata_manager.get_external_ids("123", "mock")
        assert result == {}
