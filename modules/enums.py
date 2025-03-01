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

from enum import Enum


class GGBotEnum(Enum):
    @classmethod
    def values(cls):
        return list(map(lambda c: c, cls))


class TorrentPieceSize(GGBotEnum):
    KB_16 = 16 * 1024  # 16 KiB
    KB_32 = 32 * 1024  # 32 KiB
    KB_64 = 64 * 1024  # 64 KiB
    MB_1 = 1 * 1024 * 1024  # 1 MiB
    MB_2 = 2 * 1024 * 1024  # 2 MiB
    MB_4 = 4 * 1024 * 1024  # 4 MiB
    MB_8 = 8 * 1024 * 1024  # 8 MiB
    MB_16 = 16 * 1024 * 1024  # 16 MiB
    MB_32 = 32 * 1024 * 1024  # 32 MiB
    MB_64 = 64 * 1024 * 1024  # 64 MiB
