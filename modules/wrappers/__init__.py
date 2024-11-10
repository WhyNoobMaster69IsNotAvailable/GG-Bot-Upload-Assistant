# GG Bot Upload Assistant
# Copyright (C) 2022  Noob Master669

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

import re
from typing import Optional, List


class GGBotApiCallError:
    """
    A class to represent an error that occurs during an External API call in the GG BOT.
    This class provides mechanisms to redact sensitive information and mask specific strings
    in the error messages and details.

    Attributes:
    -----------
    message : str
        The error message associated with the API call.
    status_code : Optional[int]
        The HTTP status code of the failed API call.
    details : str
        Detailed information about the error.

    Methods:
    --------
    redact_sensitive_info(patterns: Optional[dict] = None) -> None:
        Redacts sensitive information from the error message and details based on provided regex patterns.

    mask_strings(strings_to_mask: Optional[List[str]] = None) -> None:
        Masks specific strings in the error message and details with a default mask ('********').

    __repr__() -> str:
        Returns a string representation of the GGBotApiCallError object.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int],
        details: str,
        mask: Optional[List[str]],
    ):
        """
        Initializes the GGBotApiCallError object with the provided message, status code, details, and
        an optional list of strings to mask.

        The constructor automatically redacts sensitive information and masks specific strings.

        :param message: The error message associated with the API call.
        :param status_code: The HTTP status code of the failed API call.
        :param details: Detailed information about the error.
        :param mask: A list of strings that should be masked in the message and details.
        """
        self.message = message
        self.status_code = status_code
        self.details = details
        self.redact_sensitive_info()
        self.mask_strings(mask)

    def redact_sensitive_info(self, patterns: Optional[dict] = None) -> None:
        """
        Redacts sensitive information from the message and details based on provided patterns.

        If no patterns are provided, default patterns for API keys, authorization tokens, PIDs,
        emails, and passwords are used.

        :param patterns: A dictionary where keys are labels and values are regex patterns to redact.
        """
        if patterns is None:
            patterns = {
                "API Key": r"(api[_-]?key[\s=:]*)([a-zA-Z0-9-_]+)",
                "Authorization": r"(Authorization:\s*)([^\s]+)",
                "Token": r"(token[\s=:]*)([a-zA-Z0-9-_]+)",
                "Pid": r"(pid[\s=:]*)([a-zA-Z0-9-_]+)",
                "Email": r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
                "Password": r"(password[\s=:]*)([^\s]+)",
            }

        for label, pattern in patterns.items():
            self.message = re.sub(
                pattern, f"\\1[REDACTED {label}]", self.message, flags=re.IGNORECASE
            )
            self.details = re.sub(
                pattern, f"\\1[REDACTED {label}]", self.details, flags=re.IGNORECASE
            )

    def mask_strings(self, strings_to_mask: Optional[List[str]] = None) -> None:
        """
        Masks specific strings in the message and details with a given mask.

        By default, the mask is set to '********'. If no strings are provided, the method will have no effect.

        :param strings_to_mask: List of strings that should be masked.
        """
        strings_to_mask = [] if strings_to_mask is None else strings_to_mask
        for sensitive_string in strings_to_mask:
            escaped_string = re.escape(sensitive_string)
            self.message = re.sub(
                escaped_string, "********", self.message, flags=re.IGNORECASE
            )
            self.details = re.sub(
                escaped_string, "********", self.details, flags=re.IGNORECASE
            )

    def __repr__(self) -> str:
        """
        Returns a string representation of the GGBotApiCallError object.

        :return: A string that represents the GGBotApiCallError object.
        """
        return f"GGBotApiCallError(message={self.message}, status_code={self.status_code}, details={self.details})"
