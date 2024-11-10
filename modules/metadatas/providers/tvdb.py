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


class TVDBMetadataProvider(GGBotMetadataProviderBase):
    # https://thetvdb.github.io/v4-api/
    LOGIN_PATH = "{base_url}/v4/login"
    SEARCH_PATH = "{base_url}/v4/search"
    CONTENT_DETAILS_PATH = "{base_url}/v4/{content_type}/{tvdb_id}/extended"

    def __init__(self, auto_mode: bool):
        super().__init__(MetadataProvider.TVDB, auto_mode=auto_mode)
        self.auth_token = self.login()

    def login(self) -> str:
        data, error = GGBotApiCallWrapper.call(
            method="POST",
            url=self.LOGIN_PATH.format(base_url=self.base_url),
            data={"apikey": self.uploader_config.TVDB_API_KEY},
            headers={"Content-Type": "application/json"},
        )
        if error:
            print(error)
        else:
            print(data)
            if isinstance(data, dict):
                return data["data"]["token"]
        return ""

    @property
    def is_searchable(self) -> bool:
        return True

    @property
    def resolvable_external_ids(self) -> List[str]:
        return ["imdb_id", "tmdb_id"]

    @property
    def is_enabled(self) -> bool:
        return self.uploader_config.TVDB_API_KEY is not None

    @property
    def supported_content_types(self) -> List[ContentType]:
        return [ContentType.TV_SHOW, ContentType.MOVIE]

    @staticmethod
    def _get_tvdb_content_type(content_type: ContentType) -> str:
        return "series" if content_type == ContentType.TV_SHOW else content_type.value

    def _headers(self):
        return {"Authorization": f"Bearer {self.auth_token}"}

    def search(
        self, *, title: str, content_type: ContentType, year: Optional[int], **kwargs
    ) -> GGBotMetadataApiResponse:
        query_params = {
            "type": self._get_tvdb_content_type(content_type),
            "query": title,
        }
        if self.is_valid_year(year):
            query_params["year"] = year

        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.SEARCH_PATH.format(base_url=self.base_url),
            params=query_params,
            headers=self._headers(),
        )
        if error:
            print(error)
        else:
            print(data)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    def resolve_external_ids(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        return self.get_details(db_id, content_type)

    def get_details(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        query_params = {"meta": "translations"}
        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.CONTENT_DETAILS_PATH.format(
                base_url=self.base_url,
                content_type=self._get_tvdb_content_type(content_type),
                tvdb_id=db_id,
            ),
            params=query_params,
            headers=self._headers(),
        )
        if error:
            print(error)
        else:
            print(data)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)
