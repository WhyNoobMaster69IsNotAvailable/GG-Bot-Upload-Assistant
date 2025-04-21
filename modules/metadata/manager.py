from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich import box

from modules.metadata.base import MetadataManager, MetadataResult
from modules.metadata.providers.tmdb import TMDBProvider
from modules.metadata.providers.imdb_api import IMDBProvider
from modules.metadata.providers.tvdb import TVDBProvider
from modules.metadata.providers.anidb import AniDBProvider
from modules.metadata.providers.tvmaze import TVMazeProvider
from modules.metadata.providers.mal import MALProvider
from modules.metadata.providers.anilist import AniListProvider

console = Console()


class MetadataService:
    """Main service for handling metadata operations"""

    def __init__(self):
        self.manager = MetadataManager()
        self._setup_providers()

    def _setup_providers(self):
        """Setup all metadata providers"""
        # Movie/TV providers
        self.manager.register_provider("tmdb", TMDBProvider())
        self.manager.register_provider("imdb", IMDBProvider())
        self.manager.register_provider("tvdb", TVDBProvider())
        self.manager.register_provider("tvmaze", TVMazeProvider())

        # Anime providers
        self.manager.register_provider("anidb", AniDBProvider())
        self.manager.register_provider("mal", MALProvider())
        self.manager.register_provider("anilist", AniListProvider())

    def search(
        self, query: str, year: Optional[str] = None, content_type: str = "movie"
    ) -> List[MetadataResult]:
        """Search across all providers"""
        return self.manager.search(query, year, content_type)

    def get_metadata(
        self, id: str, provider: str, content_type: str = "movie"
    ) -> Optional[MetadataResult]:
        """Get metadata from a specific provider"""
        return self.manager.get_metadata(id, provider, content_type)

    def get_external_ids(
        self, id: str, provider: str, content_type: str = "movie"
    ) -> Dict[str, str]:
        """Get external IDs from a specific provider"""
        return self.manager.get_external_ids(id, provider, content_type)

    def display_search_results(
        self, results: List[MetadataResult], content_type: str = "movie"
    ):
        """Display search results in a nice table format"""
        if not results:
            console.print("[red]No results found[/red]")
            return

        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=box.HEAVY,
            border_style="dim",
        )

        # Add columns based on content type
        table.add_column("Result #", justify="center")
        table.add_column("Title", justify="center")
        table.add_column("Original Title", justify="center")
        table.add_column("Release Date", justify="center")
        table.add_column("Language", justify="center")
        table.add_column("Overview", justify="center")

        for idx, result in enumerate(results, 1):
            table.add_row(
                str(idx),
                result.title,
                result.original_title or "N/A",
                str(result.release_date) if result.release_date else "N/A",
                result.language or "N/A",
                result.overview[:100] + "..."
                if result.overview and len(result.overview) > 100
                else result.overview or "N/A",
            )

        console.print(table)

    def fill_torrent_info(
        self, torrent_info: Dict, metadata: MetadataResult, content_type: str = "movie"
    ):
        """Fill torrent info with metadata"""
        if not metadata:
            return

        # Basic info
        torrent_info["title"] = metadata.title
        torrent_info["original_title"] = metadata.original_title
        torrent_info["overview"] = metadata.overview
        torrent_info["release_date"] = metadata.release_date
        torrent_info["language"] = metadata.language

        # External IDs
        if metadata.external_ids:
            torrent_info.update(metadata.external_ids)

        # Keywords
        if metadata.keywords:
            torrent_info["keywords"] = metadata.keywords

        # Trailers
        if metadata.trailers:
            torrent_info["trailers"] = metadata.trailers

        # Content type specific info
        if content_type == "episode":
            torrent_info["series_name"] = metadata.title
            torrent_info["series_year"] = (
                metadata.release_date.year if metadata.release_date else None
            )
