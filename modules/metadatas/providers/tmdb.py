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
from typing import Optional, List, Dict

from modules.metadatas.exceptions import GGBotMetadataSearchFailureException
from modules.metadatas.providers import (
    GGBotMetadataProviderBase,
    GGBotMetadataApiResponse,
    SearchResultsTableDataSchema,
)
from modules.utils import MetadataProvider, ContentType
from modules.wrappers.api_wrapper import GGBotApiCallWrapper


class TMDBMetadataProvider(GGBotMetadataProviderBase):
    # https://developer.themoviedb.org/reference/intro/getting-started
    SEARCH_PATH = "{base_url}/3/search/{content_type}"
    EXTERNAL_IDS_PATH = "{base_url}/3/{content_type}/{tmdb_id}/external_ids"
    CONTENT_DETAILS_PATH = "{base_url}/3/{content_type}/{tmdb_id}"

    def __init__(self, auto_mode: bool):
        super().__init__(MetadataProvider.TMDB, auto_mode=auto_mode)

    @property
    def _provider_name(self) -> str:
        return "TheMovieDB"

    @property
    def is_searchable(self) -> bool:
        return True

    @property
    def is_enabled(self) -> bool:
        return self.uploader_config.TMDB_API_KEY is not None

    @property
    def resolvable_external_ids(self) -> List[MetadataProvider]:
        return [MetadataProvider.IMDB, MetadataProvider.TVDB]

    @property
    def supported_content_types(self) -> List[ContentType]:
        return [ContentType.TV_SHOW, ContentType.MOVIE]

    @staticmethod
    def _get_tmdb_content_type(content_type: ContentType) -> str:
        return "tv" if content_type == ContentType.TV_SHOW else content_type.value

    def search(
        self,
        *,
        title: str,
        content_type: ContentType,
        year: Optional[int] = None,
        **kwargs,
    ) -> GGBotMetadataApiResponse:
        query_params = {
            "page": 1,
            "include_adult": "false",
            "api_key": self.uploader_config.TMDB_API_KEY,
            "query": f"'{title}'",
        }
        if self.is_valid_year(year):
            query_params["year"] = year

        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.SEARCH_PATH.format(
                base_url=self.base_url,
                content_type=self._get_tmdb_content_type(content_type),
            ),
            params=query_params,
        )
        if error:
            return GGBotMetadataApiResponse.error(self.metadata_provider, error)

        if len(data["results"]) == 0:
            query_params["query"] = title
            data, error = GGBotApiCallWrapper.call(
                method="GET",
                url=self.SEARCH_PATH.format(
                    base_url=self.base_url,
                    content_type=self._get_tmdb_content_type(content_type),
                ),
                params=query_params,
            )
            if error:
                return GGBotMetadataApiResponse.error(self.metadata_provider, error)

        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    def resolve_external_ids(
        self, tmdb_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        query_params = {
            "api_key": self.uploader_config.TMDB_API_KEY,
            "language": "en-US",
        }

        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.CONTENT_DETAILS_PATH.format(
                base_url=self.base_url,
                content_type=self._get_tmdb_content_type(content_type),
                tmdb_id=tmdb_id,
            ),
            params=query_params,
        )
        if error:
            return GGBotMetadataApiResponse.error(self.metadata_provider, error)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    def get_details(
        self, tmdb_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        query_params = {"api_key": self.uploader_config.TMDB_API_KEY}

        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.EXTERNAL_IDS_PATH.format(
                base_url=self.base_url,
                content_type=self._get_tmdb_content_type(content_type),
                tmdb_id=tmdb_id,
            ),
            params=query_params,
        )
        if error:
            return GGBotMetadataApiResponse.error(self.metadata_provider, error)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    def process_search_results(
        self, api_response: GGBotMetadataApiResponse, content_type: ContentType
    ):
        year = ""  # TODO: get this along with GGBotMetadataApiResponse
        result_dict: Dict[int, str] = {}
        result_num = 0
        applicable_search_results = []
        for possible_match in api_response.api_response["results"]:
            result_num += 1
            result_dict[result_num] = possible_match["id"]

            release_title = self._get_release_title(possible_match)
            release_date = self._get_release_date(possible_match)
            logging.info(f"[TMDBMetadataProvider] Selected Title: [{release_title}]")
            logging.info(
                f"[TMDBMetadataProvider] Selected Release Date: [{release_date}]"
            )

            if (
                self._apply_year_based_filter(
                    content_type=content_type,
                    upload_year=year,
                    release_date=release_date,
                )
                is False
            ):
                logging.info(
                    "[TMDBMetadataProvider] The possible match failed to pass year filter."
                )
                del result_dict[result_num]
                result_num -= 1
                continue

            overview = self._get_release_overview(
                release_id=str(possible_match.get("id")),
                overview=possible_match.get("overview"),
            )
            search_data = {
                "result_num": result_num,
                "title": release_title,
                "content_type": content_type.value,
                "tmdb_id": possible_match["id"],
                "release_date": release_date,
                "language": possible_match["original_language"],
                "overview": overview,
            }
            applicable_search_results.append(search_data)
            result_data = SearchResultsTableDataSchema().load(data=search_data)
            self._add_to_search_result_table(result_data)

            if result_num < 1:
                self.console.print(
                    "Cannot auto select TMDB id. Marking upload as [bold red]TMDB_IDENTIFICATION_FAILED[/bold red]"
                )
                logging.info(
                    "[TMDBMetadataProvider] Cannot auto select TMDB id. Marking upload as TMDB_IDENTIFICATION_FAILED"
                )
                raise GGBotMetadataSearchFailureException(
                    provider=self._provider_name, message="Cannot auto select a TMDB Id"
                )

            selected = self._prompt_user_to_select_a_search_result(
                no_of_results=result_num
            )
            tmdb_id = str(result_dict[selected])

            return_response = GGBotMetadataApiResponse.create_from(api_response)
            return_response.set_tmdb_id(tmdb_id)
            return return_response

    def fill_other_database_ids(
        self, *, processed_response: GGBotMetadataApiResponse, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        external_id_api_response = self.resolve_external_ids(
            tmdb_id=processed_response.tmdb_id, content_type=content_type
        )
        if external_id_api_response.is_failure():
            return GGBotMetadataApiResponse.create_from(processed_response)

        api_response = external_id_api_response.api_response
        if api_response.get("status_message") is not None:
            logging.error(
                f"[TMDBMetadataProvider] TMDB api cal error: '{api_response['status_message']}' "
            )
            return GGBotMetadataApiResponse.create_from(processed_response)

        filled_api_response = GGBotMetadataApiResponse.create_from(processed_response)
        filled_api_response.imdb_id = api_response.get("imdb_id", "0")
        filled_api_response.tvdb_id = api_response.get("tvdb_id", "0")
        return filled_api_response

    @staticmethod
    def _apply_year_based_filter(
        *, content_type: ContentType, upload_year: str, release_date: str
    ) -> bool:
        if content_type == ContentType.TV_SHOW:
            logging.info(
                "[TMDBMetadataProvider] Skipping year matching since this is an episode."
            )
            return True

        if (
            upload_year == ""
            or int(upload_year) < 1
            or release_date == "N.A."
            or len(release_date) < 1
        ):
            return True

        year = int(upload_year)
        release_date_sub_part = int(release_date.split("-")[0])
        logging.info(
            f"[TMDBMetadataProvider] Expected years are [{year - 1}, {year}, or {year + 1}]. Obtained year [{release_date_sub_part}]"
        )

        if (
            release_date_sub_part == year
            or release_date_sub_part == year - 1
            or release_date_sub_part == year + 1
        ):
            return True
        return False

    @staticmethod
    def _get_release_date(possible_match: Dict) -> str:
        date_match = [
            possible_match[key]
            for key in possible_match
            if key in ["release_date", "first_air_date"]
        ]
        if len(date_match) == 0:
            logging.error(
                f"[TMDBMetadataProvider] Release Date not found on TMDB for TMDB ID: {str(possible_match['id'])}"
            )
            return "N.A."
        return date_match.pop()

    @staticmethod
    def _get_release_title(possible_match: Dict) -> str:
        title_match = [
            possible_match[key] for key in possible_match if key in ["title", "name"]
        ]
        if len(title_match) == 0:
            logging.error(
                f"[TMDBMetadataProvider] Title not found on TMDB for TMDB ID: {str(possible_match['id'])}"
            )
            return "N.A."
        return title_match.pop()

    @staticmethod
    def _get_release_overview(release_id: str, overview: Optional[str]):
        if overview is None or len(overview) < 1:
            logging.error(
                f"[MetadataUtils] Overview not found on TMDB for TMDB ID: {release_id}"
            )
            return "N.A."
        return overview


if __name__ == "__main__":
    # TMDBMetadataProvider(auto_mode=False).search(title="How I Met Your Mother", content_type=ContentType.TV_SHOW)
    TMDBMetadataProvider(auto_mode=False).resolve_external_ids(
        str(1100), ContentType.TV_SHOW
    )
