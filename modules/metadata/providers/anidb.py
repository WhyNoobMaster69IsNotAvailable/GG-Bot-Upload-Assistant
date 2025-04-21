import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests

from modules.config import UploaderConfig, BaseUrlConfig
from modules.metadata.base import MetadataProvider, MetadataResult


class AniDBProvider(MetadataProvider):
    """AniDB metadata provider implementation"""

    def __init__(self):
        self.config = UploaderConfig()
        self.base_url = BaseUrlConfig().ANIDB_BASE_URL
        self.client_id = self.config.ANIDB_CLIENT_ID
        self.client_version = self.config.ANIDB_CLIENT_VERSION
        self._session = requests.Session()

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to AniDB API"""
        if params is None:
            params = {}

        params.update(
            {"client": self.client_id, "clientver": self.client_version, "protover": 1}
        )

        url = f"{self.base_url}/{endpoint}"
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search AniDB for content"""
        try:
            # AniDB search is anime-focused
            if content_type == "movie":
                return []

            results = self._make_request("anime", {"title": query})
            if not results.get("anime"):
                return []

            parsed_results = []
            for result in results["anime"]:
                try:
                    # Get full anime data
                    anime = self._make_request(f"anime/{result['aid']}")
                    if not anime.get("anime"):
                        continue

                    # Filter by year if specified
                    if year and anime["anime"].get("startdate"):
                        anime_year = anime["anime"]["startdate"].split("-")[0]
                        if anime_year != year:
                            continue

                    parsed_results.append(self._parse_anime_data(anime["anime"]))
                except Exception as e:
                    logging.error(f"Failed to parse AniDB result: {e}")
                    continue

            return parsed_results
        except Exception as e:
            logging.error(f"AniDB search failed: {e}")
            return []

    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by AniDB ID"""
        try:
            if content_type == "movie":
                return None

            anime = self._make_request(f"anime/{id}")
            if not anime.get("anime"):
                return None

            return self._parse_anime_data(anime["anime"])
        except Exception as e:
            logging.error(f"Failed to get AniDB data: {e}")
            return None

    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs from AniDB"""
        try:
            if content_type == "movie":
                return {}

            anime = self._make_request(f"anime/{id}")
            if not anime.get("anime"):
                return {}

            return {
                "mal_id": anime["anime"].get("mal_id"),
                "anilist_id": anime["anime"].get("anilist_id"),
                "kitsu_id": anime["anime"].get("kitsu_id"),
            }
        except Exception as e:
            logging.error(f"Failed to get AniDB external IDs: {e}")
            return {}

    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords from AniDB"""
        try:
            if content_type == "movie":
                return []

            anime = self._make_request(f"anime/{id}")
            if not anime.get("anime"):
                return []

            return [tag["name"] for tag in anime["anime"].get("tags", [])]
        except Exception as e:
            logging.error(f"Failed to get AniDB keywords: {e}")
            return []

    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs from AniDB"""
        try:
            if content_type == "movie":
                return []

            anime = self._make_request(f"anime/{id}")
            if not anime.get("anime"):
                return []

            return [
                video["url"]
                for video in anime["anime"].get("videos", [])
                if video["type"] == "trailer"
            ]
        except Exception as e:
            logging.error(f"Failed to get AniDB trailers: {e}")
            return []

    def _parse_anime_data(self, anime: Dict) -> MetadataResult:
        """Parse AniDB anime data into MetadataResult"""
        try:
            # Get release date
            release_date = None
            if anime.get("startdate"):
                release_date = datetime.strptime(anime["startdate"], "%Y-%m-%d").date()

            return MetadataResult(
                id=str(anime["aid"]),
                title=anime.get("title", ""),
                original_title=anime.get("romaji", ""),
                overview=anime.get("description", ""),
                release_date=release_date,
                language=anime.get("language", "ja"),
                external_ids=self.get_external_ids(anime["aid"]),
                keywords=self.get_keywords(anime["aid"]),
                trailers=self.get_trailers(anime["aid"]),
            )
        except Exception as e:
            logging.error(f"Failed to parse AniDB anime data: {e}")
            return None
