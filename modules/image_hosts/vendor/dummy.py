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

from modules.image_hosts.image_host_base import GGBotImageHostBase
from modules.image_hosts.image_upload_status import GGBotImageUploadStatus


class DummyImageHost(GGBotImageHostBase):
    def __init__(self, image_path: str):
        super().__init__(image_path)

    def upload(self):
        self.upload_status = GGBotImageUploadStatus(
            status=True,
            bb_code_thumb=f'[url=http://ggbot/img1][img]{"t.".join("http://ggbot/img1".rsplit(".", 1))}[/img][/url]',
            bb_code_medium=f'[url=http://ggbot/img1][img]{"m.".join("http://ggbot/img1".rsplit(".", 1))}[/img][/url]',
            bb_code_medium_thumb=f"[url=http://ggbot/img1][img={self.thumb_size}]"
            f'{"m.".join("http://ggbot/img1".rsplit(".", 1))}[/img][/url]',
            image_url="http://ggbot/img1",
        )

    @property
    def img_host(self) -> str:
        return "DUMMY"
