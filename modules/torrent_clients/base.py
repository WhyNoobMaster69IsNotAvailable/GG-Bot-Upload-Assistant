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


from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from modules.config import ReUploaderConfig


class GGBotTorrentClientTemplate(ABC):
    def __init__(self):
        self.dynamic_tracker_selection = False

    @abstractmethod
    def hello(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def upload_torrent(
        self,
        torrent_path: str,
        save_path: str,
        use_auto_torrent_management: bool,
        is_skip_checking: bool,
        category: Optional[str] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_torrent_category(
        self, info_hash: str, category_name: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_torrents(self) -> List[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def list_all_torrents(self) -> List[Dict[str, str]]:
        raise NotImplementedError

    def get_dynamic_trackers(self, torrent: Dict[str, str]) -> List[str]:
        # a sanity check just to be sure
        if self.dynamic_tracker_selection:
            # this torrent is the translated data hence category instead of d.custom1
            category = torrent["category"]
            # removing any trailing ::
            if category.endswith("::"):
                category = category[:-2]
            trackers = category.split("::")
            return trackers[1:]  # first entry will always be GGBOT
        else:
            return []

    def _initialize_reuploader_config(self, config: ReUploaderConfig):
        self.dynamic_tracker_selection = config.DYNAMIC_TRACKER_SELECTION
        if self.dynamic_tracker_selection:
            # reuploader running in dynamic tracker selection mode
            self.target_label: str = "GGBOT"
        else:
            # `target_label` is the label of the torrents that we are interested in
            self.target_label: str = config.REUPLOAD_LABEL

        # `seed_label` is the label which will be added to the cross-seeded torrents
        self.seed_label: str = config.CROSS_SEED_LABEL
        # `source_label` is the label which will be added to the original torrent in the client
        self.source_label: str = f"{self.seed_label}_Source"
