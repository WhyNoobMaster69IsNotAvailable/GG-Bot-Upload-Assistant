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

import logging

from imgurpython import ImgurClient
from imgurpython.helpers.error import (
    ImgurClientError,
    ImgurClientRateLimitError,
)
from rich.console import Console

from modules.image_hosts.image_host_base import GGBotImageHostBase
from modules.image_hosts.image_upload_status import GGBotImageUploadStatus
from modules.config import ImgurConfig

# For more control over rich terminal content, import and construct a Console object.
console = Console()


class ImgurImageHost(GGBotImageHostBase):
    def __init__(self, image_path):
        super().__init__(image_path=image_path)
        self.config = ImgurConfig()

    @property
    def img_host(self) -> str:
        return "imgur"

    def upload(self):
        try:
            response = ImgurClient(
                client_id=self.config.CLIENT_ID,
                client_secret=self.config.API_KEY,
            ).upload_from_path(self.image_path)
            logging.debug(
                f"[ImgurImageHost::upload] Imgur image upload response: {response}"
            )
            self.upload_status = GGBotImageUploadStatus(
                status=True,
                bb_code_thumb=f'[url={response["link"]}][img]{"t.".join(response["link"].rsplit(".", 1))}[/img][/url]',
                bb_code_medium=f'[url={response["link"]}][img]{"m.".join(response["link"].rsplit(".", 1))}[/img][/url]',
                bb_code_medium_thumb=f'[url={response["link"]}][img={self.thumb_size}]{"m.".join(response["link"].rsplit(".", 1))}[/img][/url]',
                image_url=response["link"],
            )
        except TypeError or ImgurClientError or ImgurClientRateLimitError:
            logging.error(
                "[ImgurImageHost::upload] imgur upload failed, double check the imgur API Key & try again."
            )
            console.print(
                "\\imgur upload failed. double check the [bold]imgur_client_id[/bold] and in [bold]imgur_api_key["
                "/bold] [bold]config.env[/bold]\n",
                style="Red",
                highlight=False,
            )
