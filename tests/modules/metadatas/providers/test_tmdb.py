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
from unittest import mock
from unittest.mock import PropertyMock

import pytest

from modules.metadatas.providers.tmdb import TMDBMetadataProvider
from modules.utils import ContentType, MetadataProvider


class TestTMDBMetadataProvider:
    @pytest.fixture()
    def metadata_provider(self):
        return TMDBMetadataProvider(False)

    def test_resolvable_external_ids(self, metadata_provider):
        assert metadata_provider.resolvable_external_ids == [
            MetadataProvider.IMDB,
            MetadataProvider.TVDB,
        ]

    def test_supported_content_types(self, metadata_provider):
        assert metadata_provider.supported_content_types == [
            ContentType.TV_SHOW,
            ContentType.MOVIE,
        ]

    @mock.patch("modules.config.UploaderConfig.TMDB_API_KEY", new_callable=PropertyMock)
    def test_is_enabled(self, mock_api_key, metadata_provider):
        mock_api_key.return_value = "test"
        assert metadata_provider.is_enabled is True

    @mock.patch("modules.config.UploaderConfig.TMDB_API_KEY", new_callable=PropertyMock)
    def test_is_enabled_disabled_case(self, mock_api_key, metadata_provider):
        mock_api_key.return_value = None
        assert metadata_provider.is_enabled is False

    @pytest.mark.parametrize(
        ("content_type", "expected"),
        [
            pytest.param(ContentType.TV_SHOW, "tv", id="tv_shows"),
            pytest.param(ContentType.MOVIE, "movie", id=",movies"),
        ],
    )
    def test_get_tmdb_content_type(self, content_type, expected, metadata_provider):
        assert metadata_provider._get_tmdb_content_type(content_type) == expected
