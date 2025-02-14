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

import requests
from rich.console import Console

from modules.image_hosts.image_host_base import GGBotImageHostBase
from modules.image_hosts.image_upload_status import GGBotImageUploadStatus

# For more control over rich terminal content, import and construct a Console object.
console = Console()


class PixhostImageHost(GGBotImageHostBase):
    def __init__(self, image_path):
        super().__init__(image_path=image_path)

    @property
    def img_host(self) -> str:
        return "pixhost"

    def upload(self):
        data = {"content_type": "0", "max_th_size": self.thumb_size}
        files = {"img": open(self.image_path, "rb")}
        img_upload_request = requests.post(
            url="https://api.pixhost.to/images", data=data, files=files
        )

        if img_upload_request.ok:
            img_upload_response = img_upload_request.json()
            logging.debug(
                f"[PixhostImageHost::upload] Image upload response: {img_upload_response}"
            )
            image_url = (
                img_upload_response["th_url"]
                .replace("t77", "img77")
                .replace("/thumbs/", "/images/")
            )
            self.upload_status = GGBotImageUploadStatus(
                status=True,
                bb_code_medium_thumb=f'[url={img_upload_response["show_url"]}][img={self.thumb_size}]{image_url}[/img][/url]',
                bb_code_medium=f'[url={img_upload_response["show_url"]}][img]{image_url}[/img][/url]',
                bb_code_thumb=f'[url={img_upload_response["show_url"]}][img]{img_upload_response["th_url"]}[/img][/url]',
                image_url=image_url,
            )
        else:
            logging.error(
                f"[PixhostImageHost::upload] {self.img_host} upload failed. JSON Response: {img_upload_response}"
            )
            console.print(
                f"{self.img_host} upload failed. Status code: [bold]{img_upload_request.status_code}[/bold]",
                style="red3",
                highlight=False,
            )
