# GG Bot Upload Assistant
# Copyright (C) 2022  Noob Master669
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

from typing import Optional, Dict, Any, Tuple, Union, List

import requests
from requests import HTTPError, RequestException

from modules.wrappers import GGBotApiCallError


class GGBotApiCallWrapper:
    """
    A wrapper class to handle API calls within the GG Bot application.

    This class provides a static method to make HTTP requests with built-in error handling,
    response parsing, and sensitive information redaction/masking.

    Methods:
    --------
    call(
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Union[str, int]]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        mask: Optional[List[str]] = None
    ) -> Tuple[Optional[Union[Dict[str, Any], str]], Optional[GGBotApiCallError]]:
        Makes an HTTP request based on the provided parameters and returns the response data
        or an error with detailed information.
    """

    @staticmethod
    def call(
        *,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Union[str, int]]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout=10,
        mask: Optional[List[str]] = None,
    ) -> Tuple[Optional[Union[Dict[str, Any], str]], Optional[GGBotApiCallError]]:
        """
        Makes an HTTP request based on the provided parameters.

        This method handles different HTTP methods such as GET, POST, PUT, DELETE, etc.,
        and returns either the response data or a detailed error object.

        :param method: The HTTP method to use for the request (e.g., 'GET', 'POST').
        :param url: The URL to send the request to.
        :param headers: A dictionary of HTTP headers to send with the request.
        :param params: A dictionary of URL parameters to send with the request.
        :param data: A dictionary of form data to send with the request.
        :param json: A JSON object to send with the request.
        :param cookies: A dictionary of cookies to send with the request.
        :param timeout: The number of seconds to wait for the server to send data before giving up. Default is 10 seconds.
        :param mask: A list of strings that should be masked in the error message and details, if an error occurs.

        :return: A tuple containing either the response data (as a dictionary or string) and None, or None and an
                 instance of GGBotApiCallError with detailed information about the error.
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                cookies=cookies,
                timeout=timeout,
            )
            response.raise_for_status()
            try:
                return response.json(), None
            except ValueError:
                return response.text, None

        except HTTPError as http_err:
            return None, GGBotApiCallError(
                message=f"HTTP error occurred: {http_err}",
                status_code=http_err.response.status_code,
                details=http_err.response.text,
                mask=mask,
            )
        except RequestException as req_err:
            return None, GGBotApiCallError(
                message=f"Request error occurred: {req_err}",
                status_code=None,
                details=str(req_err),
                mask=mask,
            )
        except Exception as err:
            return None, GGBotApiCallError(
                message=f"An unexpected error occurred: {err}",
                status_code=None,
                details=str(err),
                mask=mask,
            )
