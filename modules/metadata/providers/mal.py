import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests
from jikanpy import Jikan

from modules.config import UploaderConfig, BaseUrlConfig
from modules.metadata.base import MetadataProvider, MetadataResult


class MALProvider(MetadataProvider):
    """MyAnimeList metadata provider implementation"""

    def __init__(self):
        self.config = UploaderConfig()
        self.base_url = BaseUrlConfig().MAL_BASE_URL
        self.client_id = self.config.MAL_CLIENT_ID
        self.jikan = Jikan()

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to MAL API"""
        if params is None:
            params = {}

        headers = {"X-MAL-CLIENT-ID": self.client_id}

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search MAL for content"""
        try:
            # MAL search is anime-focused
            if content_type == "movie":
                return []

            results = self.jikan.search("anime", query)
            if not results.get("results"):
                return []

            parsed_results = []
            for result in results["results"]:
                try:
                    # Get full anime data
                    anime = self.jikan.anime(result["mal_id"])
                    if not anime:
                        continue

                    # Filter by year if specified
                    if year and anime.get("aired_from"):
                        anime_year = anime["aired_from"].split("-")[0]
                        if anime_year != year:
                            continue

                    parsed_results.append(self._parse_anime_data(anime))
                except Exception as e:
                    logging.error(f"Failed to parse MAL result: {e}")
                    continue

            return parsed_results
        except Exception as e:
            logging.error(f"MAL search failed: {e}")
            return []

    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by MAL ID"""
        try:
            if content_type == "movie":
                return None

            anime = self.jikan.anime(id)
            if not anime:
                return None

            return self._parse_anime_data(anime)
        except Exception as e:
            logging.error(f"Failed to get MAL data: {e}")
            return None

    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs from MAL"""
        try:
            if content_type == "movie":
                return {}

            anime = self.jikan.anime(id)
            if not anime:
                return {}

            return {
                "anilist_id": anime.get("anilist_id"),
                "kitsu_id": anime.get("kitsu_id"),
                "anidb_id": anime.get("anidb_id"),
            }
        except Exception as e:
            logging.error(f"Failed to get MAL external IDs: {e}")
            return {}

    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords from MAL"""
        try:
            if content_type == "movie":
                return []

            anime = self.jikan.anime(id)
            if not anime:
                return []

            return [genre["name"] for genre in anime.get("genres", [])]
        except Exception as e:
            logging.error(f"Failed to get MAL keywords: {e}")
            return []

    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs from MAL"""
        try:
            if content_type == "movie":
                return []

            anime = self.jikan.anime(id)
            if not anime:
                return []

            return [anime.get("trailer_url")] if anime.get("trailer_url") else []
        except Exception as e:
            logging.error(f"Failed to get MAL trailers: {e}")
            return []

    def _parse_anime_data(self, anime: Dict) -> MetadataResult:
        """Parse MAL anime data into MetadataResult"""
        try:
            # Get release date
            release_date = None
            if anime.get("aired_from"):
                release_date = datetime.strptime(anime["aired_from"], "%Y-%m-%d").date()

            return MetadataResult(
                id=str(anime["mal_id"]),
                title=anime.get("title", ""),
                original_title=anime.get("title_japanese", ""),
                overview=anime.get("synopsis", ""),
                release_date=release_date,
                language=anime.get("language", "ja"),
                external_ids=self.get_external_ids(anime["mal_id"]),
                keywords=self.get_keywords(anime["mal_id"]),
                trailers=self.get_trailers(anime["mal_id"]),
            )
        except Exception as e:
            logging.error(f"Failed to parse MAL anime data: {e}")
            return None
