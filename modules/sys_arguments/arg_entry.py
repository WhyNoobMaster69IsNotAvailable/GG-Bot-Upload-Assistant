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

from typing import Optional, List, Dict, Union


class GGBotArgumentEntry:
    def __init__(
        self,
        *,
        dest,
        option_strings: Optional[str] = None,
        nargs: Optional[Union[str, int]] = None,
        required: bool = False,
        help_string: str = "",
        choices: Optional[List[str]] = None,
        action: Optional[str] = None,
    ):
        self.dest = dest
        self.option_strings = option_strings
        self.nargs = nargs
        self.required = required
        self.help_string = help_string
        self.action = action
        self.choices = choices

    def flags(self) -> List:
        if self.option_strings is None:
            return [self.dest]
        return [self.dest, self.option_strings]

    def values(self) -> Dict:
        if self.action == "store_true":
            return {
                "action": self.action,
                "required": self.required or False,
                "help": self.help_string,
            }
        return {
            "action": self.action,
            "nargs": self.nargs,
            "required": self.required or False,
            "help": self.help_string,
            "choices": self.choices,
        }
