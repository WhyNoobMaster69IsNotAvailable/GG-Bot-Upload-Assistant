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
import json
import logging
from typing import List, Optional

from modules.constants import (
    TMDB_TO_MAL_MAPPING,
    IMDB_TO_MAL_MAPPING,
    TVDB_TO_MAL_MAPPING,
)
from modules.metadatas.providers import (
    GGBotMetadataProviderBase,
    GGBotMetadataApiResponse,
)
from modules.utils import ContentType, MetadataProvider


class MALMetadataProvider(GGBotMetadataProviderBase):
    # https://myanimelist.net/apiconfig/references/api/v2#operation/anime_get
    # MAL have a beta API but because of the oauth based approach, it cannot be integrated easily.
    # The solution would need users to create an app and their own client_id and client_secret.

    def __init__(self, auto_mode: bool):
        super().__init__(MetadataProvider.MAL, auto_mode=auto_mode)

    @property
    def is_searchable(self) -> bool:
        return False

    @property
    def is_enabled(self) -> bool:
        return True

    def search(
        self, *, title: str, content_type: ContentType, year: Optional[int], **kwargs
    ) -> GGBotMetadataApiResponse:
        return GGBotMetadataApiResponse.empty(self.metadata_provider)

    def resolve_external_ids(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        return GGBotMetadataApiResponse.empty(self.metadata_provider)

    def get_details(
        self, db_id: str, content_type: ContentType
    ) -> GGBotMetadataApiResponse:
        return GGBotMetadataApiResponse.empty(self.metadata_provider)

    @property
    def resolvable_external_ids(self) -> List[str]:
        return ["tmdb", "imdb", "tvdb"]

    @property
    def supported_content_types(self) -> List[ContentType]:
        return [ContentType.TV_SHOW, ContentType.MOVIE]

    @staticmethod
    def _scan_mapping_file_for_mal_id(
        *, identifier, mapping_format, source, working_folder
    ):
        mapping_file_path = mapping_format.format(base_path=working_folder)
        try:
            with open(mapping_file_path) as mapping_file:
                logging.info(
                    f"[MALMetadataProvider] Trying to get MAL ID from {source} ID"
                )
                mapping = json.load(mapping_file)
                mal_id = mapping.get(str(identifier))

                if mal_id is not None:
                    logging.info(
                        f"[MALMetadataProvider] Obtained MAL ID as {mal_id} from {source} ID"
                    )
                    return mal_id
        except FileNotFoundError:
            logging.warning(
                f"[MALMetadataProvider] Mapping file not found at {mapping_file_path}"
            )

        return "0"

    def search_mal_id(
        self, tmdb: str, imdb: str, tvdb: str, working_folder: str
    ) -> GGBotMetadataApiResponse:
        sources = [
            (tmdb, TMDB_TO_MAL_MAPPING, "TMDB"),
            (imdb, IMDB_TO_MAL_MAPPING, "IMDB"),
            (tvdb, TVDB_TO_MAL_MAPPING, "TVDB"),
        ]
        mal_id = "0"
        for identifier, mapping_format, source in sources:
            mal_id = self._scan_mapping_file_for_mal_id(
                identifier=identifier,
                mapping_format=mapping_format,
                source=source,
                working_folder=working_folder,
            )
            if mal_id != "0":
                break

        response = GGBotMetadataApiResponse(
            metadata_provider=self.metadata_provider, api_response=None
        )
        response.set_mal_id(mal_id)
        return response
