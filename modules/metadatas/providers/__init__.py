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
import logging
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, List

from marshmallow import Schema, fields, post_load
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from modules.config import MetadataConfig, UploaderConfig
from modules.utils import MetadataProvider, ContentType


class SearchResultsTableData:
    def __init__(self, no, title, url, release_year, language, overview):
        self.no = no
        self.title = title
        self.url = url
        self.release_year = release_year
        self.language = language
        self.overview = overview

    def __repr__(self):
        return f"<SearchResultsTableData(title={self.title})>"


class SearchResultsTableDataSchema(Schema):
    no = fields.Int(required=True)
    title = fields.Str(required=True)
    url = fields.Url(required=True)
    release_year = fields.Str(required=True)
    language = fields.Str(required=True)
    overview = fields.Str(required=True)

    @post_load
    def make_search_results_table_data(self, data, **kwargs):
        return SearchResultsTableData(**data)


class GGBotMetadataApiResponse:
    def __init__(
        self,
        metadata_provider: MetadataProvider,
        api_response: Optional[Dict[str, Any]] = None,
        error=None,
    ):
        self.api_response = api_response
        self._error = error
        self.metadata_provider = metadata_provider
        self.imdb_id = "0"
        self.imdb_id_with_tt = "0"
        self.tmdb_id = "0"
        self.tvdb_id = "0"
        self.tvmaze_id = "0"
        self.mal_id = "0"

    @classmethod
    def create_from(
        cls, metadata_api_response: "GGBotMetadataApiResponse"
    ) -> "GGBotMetadataApiResponse":
        return GGBotMetadataApiResponse(
            metadata_provider=metadata_api_response.metadata_provider,
            api_response=metadata_api_response.api_response,
            error=metadata_api_response._error,
        )

    @staticmethod
    def error(metadata_provider: MetadataProvider, error) -> "GGBotMetadataApiResponse":
        return GGBotMetadataApiResponse(metadata_provider, None, error)

    @staticmethod
    def empty(metadata_provider: MetadataProvider):
        return GGBotMetadataApiResponse(metadata_provider, None)

    def is_failure(self):
        return not self.is_success()

    def is_success(self):
        return self._error is None

    def set_imdb_id(self, imdb_id: str) -> None:
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


class GGBotMetadataProviderBase(ABC):
    def __init__(self, metadata_provider: MetadataProvider, auto_mode: bool):
        self.console = Console()
        self.auto_mode = auto_mode
        self.metadata_provider = metadata_provider
        self.metadata_config = MetadataConfig()
        self.uploader_config = UploaderConfig()
        self.base_url = self.metadata_config.get_base_url(
            provider_id=self.metadata_provider.id, default=self.metadata_provider.url
        )
        self.search_results_table: Table = self._get_search_results_display_table()

    @property
    @abstractmethod
    def is_searchable(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def _provider_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_enabled(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def search(
        self, *, title: str, content_type: ContentType, year: Optional[int], **kwargs
    ) -> GGBotMetadataApiResponse:
        raise NotImplementedError

    @abstractmethod
    def resolve_external_ids(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        raise NotImplementedError

    @abstractmethod
    def get_details(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        raise NotImplementedError

    @property
    @abstractmethod
    def resolvable_external_ids(self) -> List[MetadataProvider]:
        raise NotImplementedError

    @property
    @abstractmethod
    def supported_content_types(self) -> List[ContentType]:
        raise NotImplementedError

    @staticmethod
    def is_valid_year(year: Optional[int]) -> str:
        return year is not None and year > 1000

    @abstractmethod
    def process_search_results(
        self, api_response: GGBotMetadataApiResponse, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        raise NotImplementedError

    @abstractmethod
    def fill_other_database_ids(
        self, *, processed_response: GGBotMetadataApiResponse, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        raise NotImplementedError

    def _get_search_results_display_table(self) -> Table:
        search_results_table = Table(
            show_header=True,
            header_style="bold cyan",
            box=box.HEAVY,
            border_style="dim",
        )
        search_results_table.add_column("Result #", justify="center")
        search_results_table.add_column("Title", justify="center")
        search_results_table.add_column(f"{self._provider_name} URL", justify="center")
        search_results_table.add_column("Release Date", justify="center")
        search_results_table.add_column("Language", justify="center")
        search_results_table.add_column("Overview", justify="center")
        return search_results_table

    def _add_to_search_result_table(
        self, search_result_data: SearchResultsTableData
    ) -> None:
        self.search_results_table.add_row(
            f"[chartreuse1][bold]{str(search_result_data.no)}[/bold][/chartreuse1]",
            search_result_data.title,
            search_result_data.url,
            search_result_data.release_year,
            search_result_data.language,
            search_result_data.overview,
            end_section=True,
        )

    def _prompt_user_to_select_a_search_result(
        self, no_of_results: int, auto_select_threshold: int, force_auto_select: bool
    ) -> int:
        # once the loop is done we can show the table to the user
        self.console.print(self.search_results_table, justify="center")
        # here we convert our integer that was storing the total num of results into a list
        list_of_num = [str(i) for i in range(1, no_of_results + 1)]

        if auto_select_threshold >= no_of_results:
            return self._auto_select_under_threshold()

        if force_auto_select:
            return self._auto_select_force()

        return int(
            Prompt.ask("Input the correct Result #", choices=list_of_num, default="1")
        )

    def _auto_select_force(self):
        self.console.print("Force auto selecting the #1 result from TMDB...")
        return 1

    def _auto_select_under_threshold(self):
        self.console.print("Auto selected the #1 result from TMDB...")
        logging.info(
            "[GGBotMetadataProviderBase] Auto selecting the first TMDB result "
        )
        return 1
