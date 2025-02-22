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

import argparse
from typing import Set, Optional

from modules.exceptions.exception import GGBotFatalException
from modules.sys_arguments.arg_config import GGBotArgumentConfig
from modules.sys_arguments.arg_entry import GGBotArgumentEntry
from modules.sys_arguments.arg_type import GGBotArgumentType


class GGBotArgumentParser:
    def __init__(self, argument_config: GGBotArgumentConfig):
        self._parser = argparse.ArgumentParser(
            prog=argument_config.name,
            description=argument_config.description,
            epilog=argument_config.epilog,
        )
        self._fill_arguments(argument_config)
        self.args = None
        self.parsed = False

        if len(self._parser._actions) == 0:
            raise GGBotFatalException(
                "No parser configs were specified. Currently we do not support working without arguments"
            )

    def parse_args(self):
        self.args = self._parser.parse_args()
        self.parsed = True
        return self.args

    def _fill_arguments(self, argument_config: GGBotArgumentConfig):
        self._fill_argument_group(
            group_name="Required Arguments",
            argument_groups=argument_config.get_arguments(GGBotArgumentType.REQUIRED),
        )
        self._fill_argument_group(
            group_name="Commonly Used Arguments",
            argument_groups=argument_config.get_arguments(GGBotArgumentType.COMMON),
        )
        self._fill_argument_group(
            group_name="Less Common Arguments",
            argument_groups=argument_config.get_arguments(GGBotArgumentType.UNCOMMON),
        )
        self._fill_argument_group(
            group_name="Internal Upload Arguments",
            argument_groups=argument_config.get_arguments(GGBotArgumentType.INTERNAL),
        )

    def _fill_argument_group(
        self, group_name: Optional[str], argument_groups: Set[GGBotArgumentEntry]
    ):
        if argument_groups is None or len(argument_groups) < 1 or group_name is None:
            return

        new_group = self._parser.add_argument_group(group_name)

        for argument_entry in argument_groups:
            new_group.add_argument(*argument_entry.flags(), **argument_entry.values())
