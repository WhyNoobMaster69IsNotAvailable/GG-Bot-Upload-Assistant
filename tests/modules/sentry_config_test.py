# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest
from qbittorrentapi import Unauthorized401Error

from modules.exceptions.exception import GGBotSentryCapturedException
from modules.sentry_config import SentryConfig


class TestSentryConfig:
    @pytest.fixture
    def sentry_config(self):
        yield SentryConfig()

    def test_sentry_ignored_errors(self):
        expected_ignored_errors = [
            AssertionError,
            Unauthorized401Error,
            GGBotSentryCapturedException,
        ]
        assert SentryConfig.sentry_ignored_errors() == expected_ignored_errors
