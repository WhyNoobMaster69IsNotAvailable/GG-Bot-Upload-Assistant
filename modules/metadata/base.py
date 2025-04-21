from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import date
import logging
import re
from dateutil import parser


def parse_date_string(date_str: Optional[str]) -> Optional[date]:
    """Parse a date string that may contain country information or be in various formats"""
    if not date_str:
        return None

    try:
        # Remove country information if present (e.g., "18 Jul 2008 (India)")
        date_str = re.sub(r"\s*\([^)]*\)$", "", date_str)

        # Try parsing with dateutil
        parsed_date = parser.parse(date_str)
        return parsed_date.date()
    except Exception as e:
        logging.warning(f"Failed to parse date string '{date_str}': {e}")
        return None


@dataclass
class MetadataResult:
    """Base class for metadata results from any provider"""

    id: str
    title: str
    original_title: str = None
    overview: Optional[str] = None
    release_date: Optional[Union[date, str]] = None  # Can be date object or string
    language: Optional[str] = None
    external_ids: Dict[str, str] = None
    keywords: Optional[List[str]] = None
    trailers: Optional[List[str]] = None
    provider: str = None  # The provider that returned this result

    def __post_init__(self):
        """Convert release_date to date object if it's a string"""
        if isinstance(self.release_date, str):
            self.release_date = parse_date_string(self.release_date)


class MetadataProvider(ABC):
    """Base interface for all metadata providers"""

    @abstractmethod
    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search for content by title and optional year"""
        pass

    @abstractmethod
    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by ID"""
        pass

    @abstractmethod
    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs (IMDB, TVDB, etc) for a given ID"""
        pass

    @abstractmethod
    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords/tags for a given ID"""
        pass

    @abstractmethod
    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs for a given ID"""
        pass


class MetadataManager:
    """Main class to manage metadata operations across multiple providers"""

    def __init__(self):
        self.providers: Dict[str, MetadataProvider] = {}
        # Define provider groups for different content types
        self.movie_providers = ["imdb", "tmdb"]
        self.tv_providers = ["imdb", "tmdb", "tvmaze", "tvdb"]
        self.anime_providers = ["anidb", "mal", "anilist"]

    def register_provider(self, name: str, provider: MetadataProvider):
        """Register a new metadata provider"""
        self.providers[name] = provider

    @staticmethod
    def _is_anime(result: MetadataResult) -> bool:
        """Check if a result is likely to be anime based on its properties"""
        # Check language
        if result.language and result.language.lower() in ["ja", "jpn", "japanese"]:
            return True

        # Check keywords
        if result.keywords:
            anime_keywords = {"anime", "manga", "japanese animation", "japanese anime"}
            if any(keyword.lower() in anime_keywords for keyword in result.keywords):
                return True

        # Check title and original title
        if result.original_title:
            # Check for Japanese characters in original title
            if any(
                "\u3040" <= char <= "\u309f" or "\u30a0" <= char <= "\u30ff"
                for char in result.original_title
            ):
                return True

        return False

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search across providers based on content type"""
        results = []
        # Only handle movie and episode content types
        if content_type not in ["movie", "episode"]:
            logging.error(
                f"Invalid content type: {content_type}. Must be 'movie' or 'episode'"
            )
            return results

        # Determine which providers to search based on content type
        if content_type == "movie":
            providers_to_search = self.movie_providers
        else:  # episode
            providers_to_search = self.tv_providers

        # First try the primary providers for the content type
        for provider_name in providers_to_search:
            if provider_name not in self.providers:
                continue
            try:
                provider_results = self.providers[provider_name].search(
                    query, year, content_type
                )
                if provider_results:
                    # Set the provider for each result
                    for result in provider_results:
                        result.provider = provider_name
                    results.extend(provider_results)
            except Exception as e:
                logging.error(f"Error searching {provider_name}: {e}")
                continue

        # If no results found or if results are anime, try anime providers
        if not results or (
            results and any(self._is_anime(result) for result in results)
        ):
            logging.info(
                "No results found or anime detected, searching anime providers"
            )
            for provider_name in self.anime_providers:
                if provider_name not in self.providers:
                    continue
                try:
                    provider_results = self.providers[provider_name].search(
                        query, year, "anime"
                    )
                    if provider_results:
                        # Set the provider for each result
                        for result in provider_results:
                            result.provider = provider_name
                        results.extend(provider_results)
                        # If we found anime results, we can stop searching
                        break
                except Exception as e:
                    logging.error(f"Error searching {provider_name}: {e}")
                    continue

        return results

    def get_metadata(
        self, id: str, provider: str, content_type: str = "movie"
    ) -> Optional[MetadataResult]:
        """Get metadata from a specific provider"""
        if provider not in self.providers:
            return None
        try:
            return self.providers[provider].get_by_id(id, content_type)
        except Exception:
            return None

    def get_external_ids(
        self, id: str, provider: str, content_type: str = "movie"
    ) -> Dict[str, str]:
        """Get external IDs from a specific provider"""
        if provider not in self.providers:
            return {}
        try:
            return self.providers[provider].get_external_ids(id, content_type)
        except Exception:
            return {}
