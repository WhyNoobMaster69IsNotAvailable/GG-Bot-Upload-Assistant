from modules.metadata.manager import MetadataService
from modules.metadata.base import MetadataResult, MetadataProvider, MetadataManager
from modules.metadata.providers.tmdb import TMDBProvider
from modules.metadata.providers.imdb_api import IMDBProvider
from modules.metadata.providers.tvdb import TVDBProvider
from modules.metadata.providers.anidb import AniDBProvider
from modules.metadata.providers.tvmaze import TVMazeProvider
from modules.metadata.providers.mal import MALProvider
from modules.metadata.providers.anilist import AniListProvider

__all__ = [
    "MetadataService",
    "MetadataResult",
    "MetadataProvider",
    "MetadataManager",
    "TMDBProvider",
    "IMDBProvider",
    "TVDBProvider",
    "AniDBProvider",
    "TVMazeProvider",
    "MALProvider",
    "AniListProvider",
]
