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

from typing import List, Optional

from modules.metadatas.providers import (
    GGBotMetadataProviderBase,
    GGBotMetadataApiResponse,
)
from modules.utils import ContentType, MetadataProvider
from modules.wrappers.api_wrapper import GGBotApiCallWrapper


class IMDBMetadataProvider(GGBotMetadataProviderBase):
    # https://tv-api.com/api
    SEARCH_PATH = "{base_url}/en/API/{content_type}/{api_key}/{query_string}"
    EXTERNAL_IDS_PATH = "{base_url}/en/API/ExternalSites/{api_key}/{imdb_id}"
    CONTENT_DETAILS_PATH = "{base_url}/en/API/Title/{api_key}/{imdb_id}"

    def __init__(self, auto_mode: bool):
        super().__init__(MetadataProvider.IMDB, auto_mode=auto_mode)

    @property
    def is_searchable(self) -> bool:
        return True

    @property
    def is_enabled(self) -> bool:
        return self.uploader_config.IMDB_API_KEY is not None

    @property
    def resolvable_external_ids(self) -> List[str]:
        return ["tmdb_id", "tvdb_id"]

    @property
    def supported_content_types(self) -> List[ContentType]:
        return [ContentType.TV_SHOW, ContentType.MOVIE]

    @staticmethod
    def _get_imdb_content_type(content_type: ContentType) -> str:
        return "SearchSeries" if content_type == ContentType.TV_SHOW else "SearchMovie"

    def resolve_external_ids(
        self, imdb_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.EXTERNAL_IDS_PATH.format(
                base_url=self.base_url,
                api_key=self.uploader_config.IMDB_API_KEY,
                tmdb_id=imdb_id,
            ),
        )
        if error:
            print(error)
        else:
            print(data)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    def search(
        self, *, title: str, content_type: ContentType, year: Optional[int], **kwargs
    ) -> GGBotMetadataApiResponse:
        query_string = f"{title} {year}" if self.is_valid_year(year) else title

        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.SEARCH_PATH.format(
                base_url=self.base_url,
                content_type=self._get_imdb_content_type(content_type),
                api_key=self.uploader_config.IMDB_API_KEY,
                query_string=query_string,
            ),
            mask=[self.uploader_config.IMDB_API_KEY],
        )
        if error:
            print(error)
        else:
            print(data)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    def get_details(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.CONTENT_DETAILS_PATH.format(
                base_url=self.base_url,
                api_key=self.uploader_config.IMDB_API_KEY,
                imdb_id=db_id,
            ),
        )
        if error:
            print(error)
        else:
            print(data)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)
