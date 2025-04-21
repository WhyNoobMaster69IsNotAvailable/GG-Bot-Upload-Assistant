import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests
from rich.console import Console

from modules.config import UploaderConfig
from modules.metadata.base import MetadataProvider, MetadataResult

console = Console()


class TMDBProvider(MetadataProvider):
    """TMDB metadata provider implementation"""

    def __init__(self):
        self.config = UploaderConfig()
        # self.base_url = BaseUrlConfig().TMDB_BASE_URL
        # self.api_key = self.config.TMDB_API_KEY
        self.base_url = "https://api.themoviedb.org"
        self.api_key = "23748c2268b64b6c7270e24cdb429497"

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to TMDB API"""
        if params is None:
            params = {}
        params["api_key"] = self.api_key

        url = f"{self.base_url}/3/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search TMDB for content"""
        # Convert content type for TMDB API
        content_type = "tv" if content_type == "episode" else content_type

        # Build search parameters
        params = {"query": query, "include_adult": False, "page": 1}
        if year:
            params["year"] = year

        # Try strict search first with quoted title
        results = []
        try:
            strict_results = self._make_request(
                f"search/{content_type}", {**params, "query": f"'{query}'"}
            )
            if strict_results["results"]:
                results.extend(
                    self._parse_search_results(strict_results["results"], content_type)
                )
        except Exception as e:
            logging.warning(f"Strict TMDB search failed: {e}")

        # Try liberal search without quotes
        try:
            if not results:
                liberal_results = self._make_request(f"search/{content_type}", params)
                if liberal_results["results"]:
                    results.extend(
                        self._parse_search_results(
                            liberal_results["results"], content_type
                        )
                    )
        except Exception as e:
            logging.error(f"TMDB search failed: {e}")

        return results

    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by TMDB ID"""
        content_type = "tv" if content_type == "episode" else content_type
        data = self._make_request(f"{content_type}/{id}")

        # Get additional data
        external_ids = self.get_external_ids(id, content_type)
        keywords = self.get_keywords(id, content_type)
        trailers = self.get_trailers(id, content_type)

        return MetadataResult(
            id=str(data["id"]),
            title=data.get("title") or data.get("name"),
            original_title=data.get("original_title") or data.get("original_name"),
            overview=data.get("overview"),
            release_date=datetime.strptime(
                data.get("release_date") or data.get("first_air_date"), "%Y-%m-%d"
            ).date()
            if data.get("release_date") or data.get("first_air_date")
            else None,
            language=data.get("original_language"),
            external_ids=external_ids,
            keywords=keywords,
            trailers=trailers,
        )

    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs from TMDB"""
        content_type = "tv" if content_type == "episode" else content_type
        data = self._make_request(f"{content_type}/{id}/external_ids")

        return {
            "imdb_id": data.get("imdb_id"),
            "tvdb_id": data.get("tvdb_id"),
            "facebook_id": data.get("facebook_id"),
            "instagram_id": data.get("instagram_id"),
            "twitter_id": data.get("twitter_id"),
        }

    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords from TMDB"""
        content_type = "tv" if content_type == "episode" else content_type
        data = self._make_request(f"{content_type}/{id}/keywords")
        return [keyword["name"] for keyword in data.get("keywords", [])]

    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs from TMDB"""
        content_type = "tv" if content_type == "episode" else content_type
        data = self._make_request(f"{content_type}/{id}/videos")

        trailers = []
        for video in data.get("results", []):
            if video["site"].lower() == "youtube" and video["type"].lower() in [
                "trailer",
                "teaser",
            ]:
                trailers.append(f"https://www.youtube.com/watch?v={video['key']}")
        return trailers

    def _parse_search_results(
        self, results: List[Dict], content_type: str
    ) -> List[MetadataResult]:
        """Parse TMDB search results into MetadataResult objects"""
        parsed_results = []
        for result in results:
            try:
                parsed_results.append(
                    MetadataResult(
                        id=str(result["id"]),
                        title=result.get("title") or result.get("name"),
                        original_title=result.get("original_title")
                        or result.get("original_name"),
                        overview=result.get("overview"),
                        release_date=datetime.strptime(
                            result.get("release_date") or result.get("first_air_date"),
                            "%Y-%m-%d",
                        ).date()
                        if result.get("release_date") or result.get("first_air_date")
                        else None,
                        language=result.get("original_language"),
                    )
                )
            except Exception as e:
                logging.error(f"Failed to parse TMDB result: {e}")
                continue
        return parsed_results


if __name__ == "__main__":
    tmdb = TMDBProvider()
    results = tmdb.search("The Dark Knight", content_type="movie")
    print(results)
