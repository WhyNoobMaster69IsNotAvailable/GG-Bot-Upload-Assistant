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

from modules.exceptions.exception import GGBotException


class GGBotVisorFieldValidationError(GGBotException):
    pass


class GGBotInvalidTorrentIdException(GGBotException):
    def __init__(self, torrent_id):
        super().__init__(f"Torrent with id {torrent_id} doesn't exist")


class GGBotNonUniqueTorrentIdException(GGBotException):
    def __init__(self, torrent_id):
        super().__init__(
            f"The provided torrent id [{torrent_id}] is not enough to identify a unique torrent"
        )
