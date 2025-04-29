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
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import transmission_rpc
from transmission_rpc import Torrent, Session
from modules.config import ReUploaderConfig, ClientConfig
from modules.torrent_clients.base import GGBotTorrentClientTemplate

transmission_keys = [
    "labels[0]",
    "haveValid",
    "downloadDir",
    "hashString",
    "name",
    "totalSize",
]
transmission_keys_translation = {
    "downloadDir": "save_path",
    "totalSize": "size",
    "hashString": "hash",
    "haveValid": "completed",
    "labels[0]": "category",
}


class Transmission(GGBotTorrentClientTemplate):
    """
    Client Specific Configurations
    Host, Port, Username, Password
    """

    def __init__(self):
        super().__init__()
        logging.info("[Transmission] Connecting to the Transmission instance...")
        self.client_config = ClientConfig()
        self.mission_client = transmission_rpc.Client(
            host=self.client_config.CLIENT_HOST,
            port=self.client_config.CLIENT_PORT,
            path=self.client_config.CLIENT_PATH or "/transmission/rpc",
            username=self.client_config.CLIENT_USERNAME,
            password=self.client_config.CLIENT_PASSWORD,
        )
        self.config = ReUploaderConfig()
        self._initialize_reuploader_config(self.config)

    def hello(self) -> None:
        session: Session = self.mission_client.get_session()
        print(f"Transmission Version: {session.version}")
        print(f"Transmission RPC Version: {session.rpc_version}")
        print(f"Transmission RPC SemVer: {session.rpc_version_semver}")

        logging.info(
            "[Transmission] Hello from Transmission. Obtained Transmission Session"
        )
        logging.info(f"[Transmission] Transmission Version: {session.version}")
        logging.info(f"[Transmission] Transmission RPC Version: {session.rpc_version}")
        logging.info(
            f"[Transmission] Transmission RPC SemVer: {session.rpc_version_semver}"
        )

    def list_all_torrents(self) -> List[Dict[str, str]]:
        return list(
            map(self.__extract_necessary_keys, self.mission_client.get_torrents())
        )

    def list_torrents(self) -> List[Dict[str, str]]:
        logging.debug(f"[Transmission] Listing torrents at {datetime.now()}")
        return list(
            map(
                self.__extract_necessary_keys,
                filter(self.__match_label, self.mission_client.get_torrents()),
            )
        )

    def upload_torrent(
        self,
        torrent_path: str,
        save_path: str,
        use_auto_torrent_management: bool,
        is_skip_checking: bool,
        category: Optional[str] = None,
    ) -> None:
        uploaded_torrent: Torrent = self.mission_client.add_torrent(
            torrent=Path(torrent_path),
            download_dir=save_path,
            labels=[category if category is not None else self.seed_label],
            paused=False,
        )
        logging.info(
            f"[Transmission] Uploaded torrent: {uploaded_torrent.fields['hashString']}"
        )

    def update_torrent_category(
        self, info_hash: str, category_name: Optional[str] = None
    ) -> None:
        category_name = (
            category_name if category_name is not None else self.source_label
        )
        self.mission_client.change_torrent(ids=info_hash, labels=[category_name])
        logging.info(
            f"[Transmission] Updated torrent: [{info_hash}] category to [{category_name}]"
        )

    def __match_label(self, torrent: Torrent):
        # we don't want to consider cross-seeded torrents uploaded by the bot
        labels = torrent.fields["labels"] or []
        label = labels[0] if len(labels) > 0 else ""

        if self.seed_label == label:
            return False
        # user wants to ignore labels, hence we'll consider all the torrents
        if self.target_label == "IGNORE_LABEL":
            return True
        # if dynamic tracker selection is enabled, then labels will follow the pattern GGBOT::TR1::TR2::TR3
        if self.dynamic_tracker_selection:
            return label.startswith(self.target_label)
        return label == self.target_label

    @staticmethod
    def __do_key_translation(key):
        return (
            transmission_keys_translation[key]
            if key in transmission_keys_translation
            else key
        )

    def __extract_necessary_keys(self, torrent: Torrent):
        torrent_data = {
            self.__do_key_translation(key): self.__get_key_from_torrent(torrent, key)
            for key in transmission_keys
        }
        torrent_data["save_path"] = f"{torrent_data['save_path']}/".replace("//", "/")
        torrent_data["content_path"] = (
            f"{torrent_data['save_path']}{torrent_data['name']}"
        )
        return torrent_data

    @staticmethod
    def __get_key_from_torrent(torrent: Torrent, key: str):
        match = re.match(r"([a-zA-Z_]+)\[(\d+)]", key)
        if match is None:
            return torrent.fields[key]

        key = match.group(1)
        index = int(match.group(2))
        return torrent.fields[key][index]
