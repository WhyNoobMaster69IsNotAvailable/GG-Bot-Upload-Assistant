# GG Bot Upload Assistant
# Copyright (C) 2022  Noob Master669
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Optional, List, Iterator, Tuple, Union

from modules.utils import MetadataProvider


class GGBotExternalDbMetadata:
    def __init__(self):
        self.imdb_id = "0"
        self.imdb_id_with_tt = "0"
        self.tmdb_id = "0"
        self.tvdb_id = "0"
        self.tvmaze_id = "0"
        self.mal_id = "0"

    def set_imdb_id(self, imdb_id: str) -> None:
        if imdb_id.lower().startswith("tt"):
            self.imdb_id = imdb_id[2:]
            self.imdb_id_with_tt = imdb_id
        else:
            self.imdb_id = imdb_id
            self.imdb_id_with_tt = f"tt{imdb_id}"

    def set_tmdb_id(self, tmdb_id: str) -> None:
        self.tmdb_id = tmdb_id

    def set_tvdb_id(self, tvdb_id: str) -> None:
        self.tvdb_id = tvdb_id

    def set_tvmaze_id(self, tvmaze_id: str) -> None:
        self.tvmaze_id = tvmaze_id

    def set_mal_id(self, mal_id: str) -> None:
        self.mal_id = mal_id

    def get_metadata_id(self, provider: MetadataProvider):
        if provider == MetadataProvider.IMDB:
            return self.imdb_id
        elif provider == MetadataProvider.TMDB:
            return self.tmdb_id
        elif provider == MetadataProvider.TVMAZE:
            return self.tvmaze_id
        elif provider == MetadataProvider.TVDB:
            return self.tvdb_id
        elif provider == MetadataProvider.MAL:
            return self.mal_id
        else:
            return None

    def all_ids_filled(self) -> bool:
        return all(
            self.get_metadata_id(provider) != "0"
            for provider in MetadataProvider.values()
        )

    def all_ids_missing(self) -> bool:
        return all(
            self.get_metadata_id(provider) == "0"
            for provider in MetadataProvider.values()
        )

    def filled_providers(self) -> List[MetadataProvider]:
        return [
            provider
            for provider in MetadataProvider.values()
            if self.get_metadata_id(provider) != "0"
        ]

    def missing_providers(self) -> List[MetadataProvider]:
        return [
            provider
            for provider in MetadataProvider.values()
            if self.get_metadata_id(provider) == "0"
        ]

    def set_metadata_id(self, provider: MetadataProvider, provider_id: str):
        if provider == MetadataProvider.IMDB:
            self.set_imdb_id(provider_id)
        elif provider == MetadataProvider.TMDB:
            self.set_tmdb_id(provider_id)
        elif provider == MetadataProvider.TVMAZE:
            self.set_tvmaze_id(provider_id)
        elif provider == MetadataProvider.TVDB:
            self.set_tvdb_id(provider_id)
        elif provider == MetadataProvider.MAL:
            self.set_mal_id(provider_id)
        else:
            pass  # this will never happen TODO: maybe log for the sake of logging


class GGBotMetadataOrchestratorRequest:
    """
    A class to hold various user-provided metadata IDs for different services.

    This class supports iteration over all the IDs, across all the different services.

    Attributes:
    -----------
    tmdb_id : List[str]
        List of TMDB IDs.
    imdb_id : List[str]
        List of IMDb IDs.
    tvmaze_id : List[str]
        List of TVMaze IDs.
    tvdb_id : List[str]
        List of TVDB IDs.
    mal_id : List[str]
        List of MyAnimeList IDs.

    Methods:
    --------
    _save_as_list(meta_id) -> List[str]:
        Converts the input into a list if it is not already one.

    __iter__() -> Iterator[str]:
        Returns an iterator that iterates over all the IDs across all services.
    """

    def __init__(
        self,
        *,
        title: str,
        year: Union[str, int] = None,
        tmdb_id: Optional[List[str]],
        imdb_id: Optional[List[str]],
        tvmaze_id: Optional[List[str]],
        tvdb_id: Optional[List[str]],
        mal_id: Optional[List[str]],
    ):
        """
        Initializes the GGBotUserProvidedMetadataIds object with lists of IDs.

        :param title: The title to search.
        :param year: The year obtained from the file title.
        :param tmdb_id: List of TMDB IDs.
        :param tmdb_id: List of TMDB IDs.
        :param imdb_id: List of IMDb IDs.
        :param tvmaze_id: List of TVMaze IDs.
        :param tvdb_id: List of TVDB IDs.
        :param mal_id: List of MyAnimeList IDs.
        """
        self.title = title
        self.year = str(year) if year is not None else year
        self.tmdb_id = self._save_as_list(tmdb_id)
        self.imdb_id = self._save_as_list(imdb_id)
        self.tvmaze_id = self._save_as_list(tvmaze_id)
        self.tvdb_id = self._save_as_list(tvdb_id)
        self.mal_id = self._save_as_list(mal_id)

    @staticmethod
    def _save_as_list(meta_id):
        """
        Ensures the metadata ID is stored as a list.

        :param meta_id: The metadata ID to be saved.
        :return: A list of metadata IDs.
        """
        if meta_id is None:
            return []
        if isinstance(meta_id, list):
            return meta_id
        return [meta_id]

    def __iter__(self) -> Iterator[Tuple[MetadataProvider, List[str]]]:
        """
        Iterates over all metadata IDs across all services.

        :return: An iterator over all the metadata IDs.
        """
        for meta_key, meta_val in {
            MetadataProvider.TMDB: self.tmdb_id,
            MetadataProvider.IMDB: self.imdb_id,
            MetadataProvider.TVMAZE: self.tvmaze_id,
            MetadataProvider.TVDB: self.tvdb_id,
            MetadataProvider.MAL: self.mal_id,
        }.items():
            yield tuple(meta_key, meta_val)
