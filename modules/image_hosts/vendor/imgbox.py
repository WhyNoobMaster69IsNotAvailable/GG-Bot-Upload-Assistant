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

import asyncio
import logging
import os

import pyimgbox

from modules.image_hosts.image_host_base import GGBotImageHostBase
from modules.image_hosts.image_upload_status import GGBotImageUploadStatus


class ImgboxImageHost(GGBotImageHostBase):
    def __init__(self, image_path: str, torrent_title: str):
        super().__init__(image_path)
        self.torrent_title = torrent_title

    @property
    def img_host(self) -> str:
        return "imgbox"

    def upload(self):
        if os.path.getsize(self.image_path) >= 10485760:  # Bytes
            logging.error(
                "[ImgboxImageHost::upload] Screenshot size is over imgbox limit of 10MB, Trying another host (if "
                "available) "
            )
            return
        # TODO: test imgbox image upload
        asyncio.run(self._imgbox_upload(filepaths=[self.image_path]))

    async def _imgbox_upload(self, filepaths):
        async with pyimgbox.Gallery(
            title=self.torrent_title, thumb_width=int(self.thumb_size)
        ) as gallery:
            async for submission in gallery.add(filepaths):
                logging.debug(
                    f"[ImgboxImageHost::upload] Imgbox image upload response: {submission}"
                )
                if not submission["success"]:
                    logging.error(
                        f"[ImgboxImageHost::upload] {submission['filename']}: {submission['error']}"
                    )
                    return

                logging.info(
                    f'[ImgboxImageHost::upload] imgbox edit url for {self.image_path}: {submission["edit_url"]}'
                )
                self.upload_status = GGBotImageUploadStatus(
                    status=True,
                    bb_code_medium_thumb=f'[url={submission["web_url"]}][img={self.thumb_size}]{submission["image_url"]}[/img][/url]',
                    bb_code_medium=f'[url={submission["web_url"]}][img]{submission["image_url"]}[/img][/url]',
                    bb_code_thumb=f'[url={submission["web_url"]}][img]{submission["thumbnail_url"]}[/img][/url]',
                    image_url=submission["image_url"],
                )
