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

import yaml

from modules.sys_arguments.arg_config import GGBotArgumentConfig
from modules.sys_arguments.arg_entry import GGBotArgumentEntry
from modules.sys_arguments.arg_type import GGBotArgumentType


class GGBotArgReader:
    def __init__(self, argument_config_file: str) -> None:
        self.argument_config_file = argument_config_file

    def read_and_get_config(self) -> GGBotArgumentConfig:
        with open(self.argument_config_file, "r", encoding="utf-8") as config_file:
            data = yaml.safe_load(config_file)

            argument_config = GGBotArgumentConfig(
                name=data["name"],
                description=data["description"],
                epilog=data["epilog"],
            )

            for argument_type in GGBotArgumentType.values():
                argument_entries = self._get_arguments_as_entries(
                    data["arguments"], argument_type
                )
                for entry in argument_entries:
                    argument_config.add_argument(
                        argument=entry, argument_type=argument_type
                    )

            return argument_config

    def _get_arguments_as_entries(self, arguments, argument_type: GGBotArgumentType):
        return [
            self._create_entry(argument)
            for argument in arguments.get(argument_type.value.lower(), [])
        ]

    @staticmethod
    def _create_entry(argument):
        nargs = GGBotArgReader._get_nargs(argument.get("nargs"))

        return GGBotArgumentEntry(
            dest=argument.get("destination"),
            option_strings=argument.get("optional_string"),
            nargs=nargs,
            required=argument.get("required"),
            help_string=argument.get("help"),
            action=argument.get("action"),
            choices=argument.get("choices"),
        )

    @staticmethod
    def _get_nargs(nargs):
        try:
            return int(nargs or "")
        except ValueError:
            pass
        return nargs
