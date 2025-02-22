# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669
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


from typing import Set

from modules.sys_arguments.arg_entry import GGBotArgumentEntry
from modules.sys_arguments.arg_type import GGBotArgumentType


class GGBotArgumentConfig:
    def __init__(self, name: str, description: str, epilog: str) -> None:
        self.name = name
        self.description = description
        self.epilog = epilog
        self._required_arguments: Set[GGBotArgumentEntry] = set()
        self._common_arguments: Set[GGBotArgumentEntry] = set()
        self._uncommon_arguments: Set[GGBotArgumentEntry] = set()
        self._internal_arguments: Set[GGBotArgumentEntry] = set()

    @property
    def switch(self):
        return {
            GGBotArgumentType.REQUIRED: self._required_arguments,
            GGBotArgumentType.COMMON: self._common_arguments,
            GGBotArgumentType.UNCOMMON: self._uncommon_arguments,
            GGBotArgumentType.INTERNAL: self._internal_arguments,
        }

    def add_argument(
        self, argument: GGBotArgumentEntry, argument_type: GGBotArgumentType
    ):
        self.switch[argument_type].add(argument)

    def get_arguments(
        self, argument_type: GGBotArgumentType
    ) -> Set[GGBotArgumentEntry]:
        return self.switch[argument_type]
