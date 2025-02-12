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

from typing import Union, Sequence

from qbittorrentapi import Unauthorized401Error

from modules.exceptions.exception import GGBotSentryCapturedException

ignored_log_lines = ["Outdated config.env file"]


class SentryConfig:
    @staticmethod
    def sentry_ignored_errors() -> Sequence[Union[type, str]]:
        return [
            AssertionError,
            Unauthorized401Error,
            GGBotSentryCapturedException,
        ]

    @staticmethod
    def before_send(event, hint):
        if any(log_line in str(event) for log_line in ignored_log_lines):
            return None
        return event
