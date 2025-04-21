import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests

from modules.config import UploaderConfig, BaseUrlConfig
from modules.metadata.base import MetadataProvider, MetadataResult


class AniListProvider(MetadataProvider):
    """AniList metadata provider implementation"""

    def __init__(self):
        self.config = UploaderConfig()
        self.base_url = BaseUrlConfig().ANILIST_BASE_URL
        self.client_id = self.config.ANILIST_CLIENT_ID
        self.client_secret = self.config.ANILIST_CLIENT_SECRET
        self._token = None

    def _get_token(self) -> str:
        """Get AniList API token"""
        if self._token:
            return self._token

        response = requests.post(
            f"{self.base_url}/auth/access_token",
            json={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
        return self._token

    def _make_request(self, query: str, variables: Dict = None) -> Dict:
        """Make a GraphQL request to AniList API"""
        if variables is None:
            variables = {}

        headers = {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.base_url,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search AniList for content"""
        try:
            # AniList search is anime-focused
            if content_type == "movie":
                return []

            search_query = """
            query ($search: String) {
                Page (page: 1, perPage: 10) {
                    media (search: $search, type: ANIME) {
                        id
                        title {
                            romaji
                            english
                            native
                        }
                        description
                        startDate {
                            year
                            month
                            day
                        }
                        genres
                        externalLinks {
                            url
                            site
                        }
                        trailer {
                            id
                            site
                        }
                    }
                }
            }
            """

            results = self._make_request(search_query, {"search": query})
            if not results.get("data", {}).get("Page", {}).get("media"):
                return []

            parsed_results = []
            for result in results["data"]["Page"]["media"]:
                try:
                    # Filter by year if specified
                    if year and result.get("startDate", {}).get("year"):
                        if str(result["startDate"]["year"]) != year:
                            continue

                    parsed_results.append(self._parse_anime_data(result))
                except Exception as e:
                    logging.error(f"Failed to parse AniList result: {e}")
                    continue

            return parsed_results
        except Exception as e:
            logging.error(f"AniList search failed: {e}")
            return []

    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by AniList ID"""
        try:
            if content_type == "movie":
                return None

            query = """
            query ($id: Int) {
                Media (id: $id) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    startDate {
                        year
                        month
                        day
                    }
                    genres
                    externalLinks {
                        url
                        site
                    }
                    trailer {
                        id
                        site
                    }
                }
            }
            """

            result = self._make_request(query, {"id": int(id)})
            if not result.get("data", {}).get("Media"):
                return None

            return self._parse_anime_data(result["data"]["Media"])
        except Exception as e:
            logging.error(f"Failed to get AniList data: {e}")
            return None

    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs from AniList"""
        try:
            if content_type == "movie":
                return {}

            query = """
            query ($id: Int) {
                Media (id: $id) {
                    id
                    externalLinks {
                        url
                        site
                    }
                }
            }
            """

            result = self._make_request(query, {"id": int(id)})
            if not result.get("data", {}).get("Media"):
                return {}

            external_ids = {}
            for link in result["data"]["Media"]["externalLinks"]:
                site = link["site"].lower()
                if site in ["myanimelist", "anidb", "kitsu"]:
                    external_ids[f"{site}_id"] = link["url"].split("/")[-1]
            return external_ids
        except Exception as e:
            logging.error(f"Failed to get AniList external IDs: {e}")
            return {}

    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords from AniList"""
        try:
            if content_type == "movie":
                return []

            query = """
            query ($id: Int) {
                Media (id: $id) {
                    id
                    genres
                    tags {
                        name
                    }
                }
            }
            """

            result = self._make_request(query, {"id": int(id)})
            if not result.get("data", {}).get("Media"):
                return []

            media = result["data"]["Media"]
            return media.get("genres", []) + [
                tag["name"] for tag in media.get("tags", [])
            ]
        except Exception as e:
            logging.error(f"Failed to get AniList keywords: {e}")
            return []

    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs from AniList"""
        try:
            if content_type == "movie":
                return []

            query = """
            query ($id: Int) {
                Media (id: $id) {
                    id
                    trailer {
                        id
                        site
                    }
                }
            }
            """

            result = self._make_request(query, {"id": int(id)})
            if not result.get("data", {}).get("Media"):
                return []

            trailer = result["data"]["Media"]["trailer"]
            if not trailer:
                return []

            if trailer["site"] == "youtube":
                return [f"https://www.youtube.com/watch?v={trailer['id']}"]
            return []
        except Exception as e:
            logging.error(f"Failed to get AniList trailers: {e}")
            return []

    def _parse_anime_data(self, anime: Dict) -> MetadataResult:
        """Parse AniList anime data into MetadataResult"""
        try:
            # Get release date
            release_date = None
            if anime.get("startDate", {}).get("year"):
                start_date = anime["startDate"]
                release_date = datetime.strptime(
                    f"{start_date['year']}-{start_date.get('month', 1)}-{start_date.get('day', 1)}",
                    "%Y-%m-%d",
                ).date()

            return MetadataResult(
                id=str(anime["id"]),
                title=anime["title"].get("english", "")
                or anime["title"].get("romaji", ""),
                original_title=anime["title"].get("native", "")
                or anime["title"].get("romaji", ""),
                overview=anime.get("description", ""),
                release_date=release_date,
                language="ja",  # AniList is primarily for Japanese content
                external_ids=self.get_external_ids(anime["id"]),
                keywords=self.get_keywords(anime["id"]),
                trailers=self.get_trailers(anime["id"]),
            )
        except Exception as e:
            logging.error(f"Failed to parse AniList anime data: {e}")
            return None
