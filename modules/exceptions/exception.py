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


class GGBotException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GGBotFatalException(GGBotException):
    pass


class GGBotSentryCapturedException(GGBotException):
    pass


class GGBotUploaderException(GGBotException):
    pass


class GGBotCacheClientException(GGBotUploaderException):
    pass


class GGBotCacheNotInitializedException(GGBotCacheClientException):
    def __init__(self):
        super().__init__("Connection to cache not established")


class GGBotRetryException(GGBotException):
    pass


class GGBotConfigException(GGBotException):
    pass
