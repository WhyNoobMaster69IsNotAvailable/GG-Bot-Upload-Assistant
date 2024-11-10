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

import pytest

from modules.metadatas.providers.tvmaze import TvMazeMetadataProvider
from modules.utils import ContentType


class TestTvMazeMetadataProvider:
    @pytest.fixture()
    def metadata_provider(self):
        return TvMazeMetadataProvider(False)

    def test_resolvable_external_ids(self, metadata_provider):
        assert metadata_provider.resolvable_external_ids == [
            "tvrage_id",
            "tvdb_id",
            "imdb_id",
        ]

    def test_is_enabled(self, metadata_provider):
        assert metadata_provider.is_enabled is True

    def test_supported_content_types(self, metadata_provider):
        assert metadata_provider.supported_content_types == [ContentType.TV_SHOW]
