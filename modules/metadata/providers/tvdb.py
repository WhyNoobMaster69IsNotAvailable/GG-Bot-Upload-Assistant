import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests

from modules.config import UploaderConfig, BaseUrlConfig
from modules.metadata.base import MetadataProvider, MetadataResult


class TVDBProvider(MetadataProvider):
    """TVDB metadata provider implementation"""

    def __init__(self):
        self.config = UploaderConfig()
        self.base_url = BaseUrlConfig().TVDB_BASE_URL
        self.api_key = self.config.TVDB_API_KEY
        self._token = None

    def _get_token(self) -> str:
        """Get TVDB API token"""
        if self._token:
            return self._token

        response = requests.post(
            f"{self.base_url}/login", json={"apikey": self.api_key}
        )
        response.raise_for_status()
        self._token = response.json()["token"]
        return self._token

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to TVDB API"""
        if params is None:
            params = {}

        headers = {"Authorization": f"Bearer {self._get_token()}"}

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search TVDB for content"""
        try:
            # TVDB search is TV-focused
            if content_type == "movie":
                return []

            results = self._make_request("search/series", {"name": query})
            if not results.get("data"):
                return []

            parsed_results = []
            for result in results["data"]:
                try:
                    # Get full series data
                    series = self._make_request(f"series/{result['id']}")
                    if not series.get("data"):
                        continue

                    # Filter by year if specified
                    if year and series["data"].get("firstAired"):
                        series_year = series["data"]["firstAired"].split("-")[0]
                        if series_year != year:
                            continue

                    parsed_results.append(self._parse_series_data(series["data"]))
                except Exception as e:
                    logging.error(f"Failed to parse TVDB result: {e}")
                    continue

            return parsed_results
        except Exception as e:
            logging.error(f"TVDB search failed: {e}")
            return []

    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by TVDB ID"""
        try:
            if content_type == "movie":
                return None

            series = self._make_request(f"series/{id}")
            if not series.get("data"):
                return None

            return self._parse_series_data(series["data"])
        except Exception as e:
            logging.error(f"Failed to get TVDB data: {e}")
            return None

    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs from TVDB"""
        try:
            if content_type == "movie":
                return {}

            series = self._make_request(f"series/{id}/externalIds")
            if not series.get("data"):
                return {}

            return {
                "imdb_id": series["data"].get("imdbId"),
                "tmdb_id": series["data"].get("tmdbId"),
                "zap2it_id": series["data"].get("zap2itId"),
            }
        except Exception as e:
            logging.error(f"Failed to get TVDB external IDs: {e}")
            return {}

    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords from TVDB"""
        try:
            if content_type == "movie":
                return []

            series = self._make_request(f"series/{id}/tags")
            if not series.get("data"):
                return []

            return [tag["name"] for tag in series["data"]]
        except Exception as e:
            logging.error(f"Failed to get TVDB keywords: {e}")
            return []

    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs from TVDB"""
        try:
            if content_type == "movie":
                return []

            series = self._make_request(f"series/{id}/episodes")
            if not series.get("data"):
                return []

            trailers = []
            for episode in series["data"]:
                if episode.get("filename"):
                    trailers.append(episode["filename"])
            return trailers
        except Exception as e:
            logging.error(f"Failed to get TVDB trailers: {e}")
            return []

    def _parse_series_data(self, series: Dict) -> MetadataResult:
        """Parse TVDB series data into MetadataResult"""
        try:
            # Get release date
            release_date = None
            if series.get("firstAired"):
                release_date = datetime.strptime(
                    series["firstAired"], "%Y-%m-%d"
                ).date()

            return MetadataResult(
                id=str(series["id"]),
                title=series.get("seriesName", ""),
                original_title=series.get(
                    "seriesName", ""
                ),  # TVDB doesn't have original titles
                overview=series.get("overview", ""),
                release_date=release_date,
                language=series.get("language", "en"),
                external_ids=self.get_external_ids(series["id"]),
                keywords=self.get_keywords(series["id"]),
                trailers=self.get_trailers(series["id"]),
            )
        except Exception as e:
            logging.error(f"Failed to parse TVDB series data: {e}")
            return None
