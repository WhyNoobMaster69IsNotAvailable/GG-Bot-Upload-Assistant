import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests

from modules.config import UploaderConfig, BaseUrlConfig
from modules.metadata.base import MetadataProvider, MetadataResult


class TVMazeProvider(MetadataProvider):
    """TVMaze metadata provider implementation"""

    def __init__(self):
        self.config = UploaderConfig()
        self.base_url = BaseUrlConfig().TVMAZE_BASE_URL

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to TVMaze API"""
        if params is None:
            params = {}

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search TVMaze for content"""
        try:
            # TVMaze search is TV-focused
            if content_type == "movie":
                return []

            results = self._make_request("search/shows", {"q": query})
            if not results:
                return []

            parsed_results = []
            for result in results:
                try:
                    # Get full show data
                    show = result.get("show", {})
                    if not show:
                        continue

                    # Filter by year if specified
                    if year and show.get("premiered"):
                        show_year = show["premiered"].split("-")[0]
                        if show_year != year:
                            continue

                    parsed_results.append(self._parse_show_data(show))
                except Exception as e:
                    logging.error(f"Failed to parse TVMaze result: {e}")
                    continue

            return parsed_results
        except Exception as e:
            logging.error(f"TVMaze search failed: {e}")
            return []

    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by TVMaze ID"""
        try:
            if content_type == "movie":
                return None

            show = self._make_request(f"shows/{id}")
            if not show:
                return None

            return self._parse_show_data(show)
        except Exception as e:
            logging.error(f"Failed to get TVMaze data: {e}")
            return None

    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs from TVMaze"""
        try:
            if content_type == "movie":
                return {}

            show = self._make_request(f"shows/{id}")
            if not show:
                return {}

            return {
                "imdb_id": show.get("externals", {}).get("imdb"),
                "tvdb_id": show.get("externals", {}).get("thetvdb"),
                "tvrage_id": show.get("externals", {}).get("tvrage"),
            }
        except Exception as e:
            logging.error(f"Failed to get TVMaze external IDs: {e}")
            return {}

    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords from TVMaze"""
        try:
            if content_type == "movie":
                return []

            show = self._make_request(f"shows/{id}")
            if not show:
                return []

            return [genre for genre in show.get("genres", [])]
        except Exception as e:
            logging.error(f"Failed to get TVMaze keywords: {e}")
            return []

    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs from TVMaze"""
        try:
            if content_type == "movie":
                return []

            show = self._make_request(f"shows/{id}")
            if not show:
                return []

            return [
                link["url"]
                for link in show.get("_links", {})
                .get("previousepisode", {})
                .get("href", [])
            ]
        except Exception as e:
            logging.error(f"Failed to get TVMaze trailers: {e}")
            return []

    def _parse_show_data(self, show: Dict) -> MetadataResult:
        """Parse TVMaze show data into MetadataResult"""
        try:
            # Get release date
            release_date = None
            if show.get("premiered"):
                release_date = datetime.strptime(show["premiered"], "%Y-%m-%d").date()

            return MetadataResult(
                id=str(show["id"]),
                title=show.get("name", ""),
                original_title=show.get(
                    "name", ""
                ),  # TVMaze doesn't have original titles
                overview=show.get("summary", ""),
                release_date=release_date,
                language=show.get("language", "en"),
                external_ids=self.get_external_ids(show["id"]),
                keywords=self.get_keywords(show["id"]),
                trailers=self.get_trailers(show["id"]),
            )
        except Exception as e:
            logging.error(f"Failed to parse TVMaze show data: {e}")
            return None
