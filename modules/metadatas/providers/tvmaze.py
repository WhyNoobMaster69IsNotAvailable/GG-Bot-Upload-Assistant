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


class TvMazeMetadataProvider(GGBotMetadataProviderBase):
    # https://www.tvmaze.com/api
    SEARCH_PATH = "{base_url}/search/shows?q=girls"
    CONTENT_DETAILS_PATH = "{base_url}/shows/{tvmaze_id}"

    def __init__(self, auto_mode: bool):
        super().__init__(MetadataProvider.TVMAZE, auto_mode=auto_mode)

    @property
    def is_searchable(self) -> bool:
        return True

    @property
    def is_enabled(self) -> bool:
        return True

    def search(
        self, *, title: str, content_type: ContentType, year: Optional[int], **kwargs
    ) -> GGBotMetadataApiResponse:
        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.SEARCH_PATH.format(base_url=self.base_url),
            params={"q": title},
        )
        if error:
            print(error)
        else:
            print(data)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    def resolve_external_ids(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        return self.get_details(db_id=db_id, content_type=content_type)

    def get_details(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        data, error = GGBotApiCallWrapper.call(
            method="GET",
            url=self.CONTENT_DETAILS_PATH.format(
                base_url=self.base_url, tvmaze_id=db_id
            ),
        )
        if error:
            print(error)
        else:
            print(data)
        return GGBotMetadataApiResponse(self.metadata_provider, api_response=data)

    @property
    def resolvable_external_ids(self) -> List[str]:
        return ["tvrage_id", "tvdb_id", "imdb_id"]

    @property
    def supported_content_types(self) -> List[ContentType]:
        return [ContentType.TV_SHOW]
