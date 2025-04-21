import logging
from datetime import datetime
from typing import Dict, List, Optional
from imdb import Cinemagoer
from imdb.Movie import Movie
import re
from dateutil import parser

from modules.metadata.base import MetadataProvider, MetadataResult


def parse_imdb_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse IMDB date string that may contain country information"""
    if not date_str:
        return None

    try:
        # Remove country information if present (e.g., "18 Jul 2008 (India)")
        date_str = re.sub(r"\s*\([^)]*\)$", "", date_str)

        # Try parsing with dateutil
        return parser.parse(date_str)
    except Exception as e:
        logging.warning(f"Failed to parse IMDB date string '{date_str}': {e}")
        return None


class IMDBProvider(MetadataProvider):
    """IMDB metadata provider implementation"""

    def __init__(self):
        self.ia = Cinemagoer()

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search IMDB for content"""
        try:
            # IMDB search doesn't support content type filtering directly
            if content_type == "movie":
                results = self.ia.search_movie(query)
            else:
                results = self.ia.search_episode(query)
            if not results:
                return []

            parsed_results = []
            for result in results:
                try:
                    # Get full movie data
                    if content_type == "movie":
                        movie = self.ia.get_movie(result.movieID)
                    else:
                        movie = self.ia.get_episode(result.episodeID)
                    if not movie:
                        continue

                    # Filter by year if specified
                    if year and movie.get("year"):
                        if str(movie["year"]) != year:
                            continue

                    parsed_results.append(self._parse_movie_data(movie))
                except Exception as e:
                    logging.error(f"Failed to parse IMDB result: {e}")
                    continue

            return parsed_results
        except Exception as e:
            logging.error(f"IMDB search failed: {e}")
            return []

    def get_by_id(self, id: str, content_type: str = "movie") -> MetadataResult:
        """Get metadata by IMDB ID"""
        try:
            # Remove 'tt' prefix if present
            clean_id = id.replace("tt", "")
            movie = self.ia.get_movie(clean_id)
            if not movie:
                return None
            return self._parse_movie_data(movie)
        except Exception as e:
            logging.error(f"Failed to get IMDB data: {e}")
            return None

    def get_external_ids(self, id: str, content_type: str = "movie") -> Dict[str, str]:
        """Get external IDs from IMDB"""
        try:
            clean_id = id.replace("tt", "")
            movie = self.ia.get_movie(clean_id)
            if not movie:
                return {}

            return {"tmdb_id": movie.get("tmdb_id"), "tvdb_id": movie.get("tvdb_id")}
        except Exception as e:
            logging.error(f"Failed to get IMDB external IDs: {e}")
            return {}

    def get_keywords(self, id: str, content_type: str = "movie") -> List[str]:
        """Get keywords from IMDB"""
        try:
            clean_id = id.replace("tt", "")
            movie = self.ia.get_movie(clean_id)
            if not movie:
                return []
            return movie.get("keywords", [])
        except Exception as e:
            logging.error(f"Failed to get IMDB keywords: {e}")
            return []

    def get_trailers(self, id: str, content_type: str = "movie") -> List[str]:
        """Get trailer URLs from IMDB"""
        try:
            clean_id = id.replace("tt", "")
            movie = self.ia.get_movie(clean_id)
            if not movie:
                return []
            return movie.get("trailers", [])
        except Exception as e:
            logging.error(f"Failed to get IMDB trailers: {e}")
            return []

    @staticmethod
    def _parse_movie_data(movie: Movie) -> MetadataResult:
        """Parse IMDB movie data into MetadataResult"""
        try:
            # Get release date
            release_date = None
            if movie.get("original air date"):
                parsed_date = parse_imdb_date(movie["original air date"])
                if parsed_date:
                    release_date = parsed_date.date()
            elif movie.get("year"):
                release_date = datetime.strptime(
                    f"{movie['year']}-01-01", "%Y-%m-%d"
                ).date()

            return MetadataResult(
                id=f"tt{movie.movieID}",
                title=movie.get("title", ""),
                original_title=movie.get("original title", ""),
                overview=movie.get("plot outline", ""),
                release_date=release_date,
                language=movie.get("languages", ["en"])[0]
                if movie.get("languages")
                else None,
                # external_ids=self.get_external_ids(movie.movieID),
                # keywords=self.get_keywords(movie.movieID),
                # trailers=self.get_trailers(movie.movieID)
            )
        except Exception as e:
            logging.error(f"Failed to parse IMDB movie data: {e}")
            return None


if __name__ == "__main__":
    imdb = IMDBProvider()
    movies = imdb.search("The Dark Knight", content_type="movie")
    print(movies)
