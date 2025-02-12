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

import base64
from typing import Dict

from modules.image_hosts.vendor.chevereto.chevereto_base import (
    CheveretoImageHostBase,
)


class ImgbbImageHost(CheveretoImageHostBase):
    @property
    def files(self) -> Dict:
        return {}

    @property
    def headers(self) -> Dict:
        return {}

    @property
    def data(self) -> Dict:
        return {
            "key": self.api_key,
            "image": base64.b64encode(open(self.image_path, "rb").read()),
        }

    @property
    def img_host(self) -> str:
        return "imgbb"

    @property
    def response_data_key(self) -> str:
        return "data"

    @property
    def url(self) -> str:
        return "https://api.imgbb.com/1/upload"
