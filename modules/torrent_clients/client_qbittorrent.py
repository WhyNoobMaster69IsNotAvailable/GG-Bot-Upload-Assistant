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

import logging
from datetime import datetime
from typing import Optional

import qbittorrentapi

from modules.config import ClientConfig, ReUploaderConfig
from modules.torrent_clients.base import GGBotTorrentClientTemplate

qbt_keys = [
    "category",
    "completed",
    "content_path",
    "hash",
    "name",
    "save_path",
    "size",
    "tracker",
]


class Qbittorrent(GGBotTorrentClientTemplate):
    """
    Client Specific Configurations
    Host, Port, Username, Password
    """

    def __init__(self):
        super().__init__()
        logging.info("[Qbittorrent] Connecting to the qbittorrent instance...")
        self.client_config = ClientConfig()
        self.reuploader_config = ReUploaderConfig()
        self.qbt_client = qbittorrentapi.Client(
            host=self.client_config.CLIENT_HOST,
            port=self.client_config.CLIENT_PORT,
            username=self.client_config.CLIENT_USERNAME,
            password=self.client_config.CLIENT_PASSWORD,
        )

        self._initialize_reuploader_config(self.reuploader_config)

        try:
            logging.info(
                "[Qbittorrent] Authenticating with the qbittorrent instance..."
            )
            self.qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as err:
            logging.fatal(
                "[Qbittorrent] Authentication with qbittorrent instance failed"
            )
            raise err

    def hello(self):
        logging.info(
            f"[Qbittorrent] Hello from qbittorrent {self.qbt_client.app.version} and web api {self.qbt_client.app.web_api_version}"
        )
        print(f"qBittorrent: {self.qbt_client.app.version}")
        print(f"qBittorrent Web API: {self.qbt_client.app.web_api_version}")

    def __match_label(self, torrent):
        # we don't want to consider cross-seeded torrents uploaded by the bot
        if self.seed_label == torrent.category:
            return False
        # user wants to ignore labels, hence we'll consider all the torrents
        if self.target_label == "IGNORE_LABEL":
            return True
        # if dynamic tracker selection is enabled, then labels will follow the pattern GGBOT::TR1::TR2::TR3
        if self.dynamic_tracker_selection:
            return torrent.category.startswith(self.target_label)
        else:
            return torrent.category == self.target_label

    @staticmethod
    def __extract_necessary_keys(torrent):
        return {key: value for key, value in torrent.items() if key in qbt_keys}

    # torrents_set_category
    def __list_categories(self):
        return self.__get_torrent_categories().categories

    def __get_torrent_categories(self):
        return self.qbt_client.torrent_categories

    def __create_category(self, name, save_path):
        self.__get_torrent_categories().create_category(name=name, save_path=save_path)

    def list_all_torrents(self):
        return list(map(self.__extract_necessary_keys, self.qbt_client.torrents_info()))

    def list_torrents(self):
        logging.debug(f"[Qbittorrent] Listing torrents at {datetime.now()}")
        return list(
            map(
                self.__extract_necessary_keys,
                filter(self.__match_label, self.qbt_client.torrents_info()),
            )
        )

    def upload_torrent(
        self,
        torrent_path,
        save_path,
        use_auto_torrent_management,
        is_skip_checking,
        category=None,
    ):
        self.qbt_client.torrents_add(
            torrent_files=torrent_path,
            save_path=save_path,
            category=category if category is not None else self.seed_label,
            use_auto_torrent_management=use_auto_torrent_management,
            is_skip_checking=is_skip_checking,
        )
        # self.qbt_client.torrents_resume(info_hash)

    def update_torrent_category(
        self, info_hash: str, category_name: Optional[str] = None
    ) -> None:
        category_name = self.source_label if category_name is None else category_name

        if category_name not in list(self.__list_categories()):
            # if the category  `category_name` doesn't exist we create it
            self.__create_category(category_name, None)

        self.qbt_client.torrents_set_category(
            category=category_name, torrent_hashes=info_hash
        )
