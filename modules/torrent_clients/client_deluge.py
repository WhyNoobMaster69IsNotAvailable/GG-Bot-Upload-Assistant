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
import base64
import logging
import time
from datetime import datetime
from typing import List, Dict, Optional

import deluge_client

from modules.config import ClientConfig, ReUploaderConfig
from modules.exceptions.exception import GGBotFatalException
from modules.torrent_clients.base import GGBotTorrentClientTemplate

deluge_keys = ["hash", "save_path", "total_done", "total_wanted", "name", "label"]

deluge_keys_translation = {
    "total_wanted": "size",
    "total_done": "completed",
    "label": "category",
}


class Deluge(GGBotTorrentClientTemplate):
    retry_limit = 10
    retry_interval = 5

    def __init__(self):
        super().__init__()
        logging.info("[Deluge] Connecting to the deluge instance...")
        self.client = self._create_client()

        self.config = ReUploaderConfig()
        self._initialize_reuploader_config(self.config)

    def _create_client(self):
        client_config = ClientConfig()
        try:
            self.client = deluge_client.DelugeRPCClient(
                host=client_config.CLIENT_HOST,
                port=int(client_config.CLIENT_PORT),
                username=client_config.CLIENT_USERNAME,
                password=client_config.CLIENT_PASSWORD,
            )
            self.client.connect()
            if self.client.connected:
                return self.client

            logging.fatal("[Deluge] Failed to connect to the deluge instance.")
            logging.info(
                "[Deluge] Ensure that remote connections are enabled by the daemon."
            )
            raise GGBotFatalException(
                "Failed to connect to the configured deluge instance. "
                "Ensure that remote connections are enabled by the daemon."
            )

        except ConnectionRefusedError as e:
            logging.error(
                "[Deluge] Failed to connect to the deluge instance. Please recheck the configurations.",
                exc_info=e,
            )
            raise GGBotFatalException(e)
        except GGBotFatalException as e:
            raise e
        except Exception as e:
            logging.error(
                f"[Deluge] Failed to connect to the deluge instance. {e}", exc_info=e
            )
            raise GGBotFatalException(e)

    def hello(self) -> None:
        logging.info(
            f"[Deluge] Hello from deluge v{self.__call_retry('daemon.get_version').decode('utf-8')} "
            f"with libtorrent version {self.__call_retry('daemon.get_version').decode('utf-8')}"
        )
        print(
            f"Deluge version: {self.__call_retry('daemon.get_version').decode('utf-8')}"
        )
        print(
            f"Deluge libtorrent version: {self.__call_retry('daemon.get_version').decode('utf-8')}"
        )

    def upload_torrent(
        self,
        torrent_path: str,
        save_path: str,
        use_auto_torrent_management: bool,
        is_skip_checking: bool,
        category: Optional[str] = None,
    ) -> None:
        category = category if category is not None else self.seed_label
        category = category.lower()

        self._check_and_create_label(category)
        with open(torrent_path, "rb") as torrent_data:
            options = {"download_location": save_path, "seed_mode": is_skip_checking}
            torrent_data_encoded = base64.b64encode(torrent_data.read())
            torrent: bytes = self.__call_retry(
                "core.add_torrent_file", torrent_path, torrent_data_encoded, options
            )
            self.update_torrent_category(torrent.decode("utf-8"), category)

    def _check_and_create_label(self, label: Optional[str]) -> None:
        if label is None:
            return
        all_labels = self.__call_retry("label.get_labels")
        if label.lower().encode("utf-8") not in all_labels:
            self.__call_retry("label.add", label.lower())

    def update_torrent_category(
        self, info_hash: str, category_name: Optional[str] = None
    ) -> None:
        category_name = (
            category_name if category_name is not None else self.source_label
        )
        category_name = category_name.lower()

        self._check_and_create_label(category_name)
        self.__call_retry("label.set_torrent", info_hash, category_name)
        logging.info(
            f"[Deluge] Updated torrent: [{info_hash}] category to [{category_name}]"
        )

    def list_torrents(self) -> List[Dict[str, str]]:
        logging.debug(f"[Deluge] Listing torrents at {datetime.now()}")
        torrents = self.__call_retry("core.get_torrents_status", {}, [])
        if torrents is None:
            return []
        return list(
            map(
                self.__extract_necessary_keys,
                filter(self.__match_label, torrents.values()),
            )
        )

    def list_all_torrents(self) -> List[Dict[str, str]]:
        torrents = self.__call_retry("core.get_torrents_status", {}, [])
        if torrents is None:
            return []
        return list(map(self.__extract_necessary_keys, torrents.values()))

    def __call_retry(self, method, *args, **kwargs):
        for attempt in range(self.retry_limit):
            try:
                return self.client.call(method, *args, **kwargs)
            except deluge_client.FailedToReconnectException as e:
                if attempt >= self.retry_interval:
                    raise e
                time.sleep(self.retry_interval)

    def __match_label(self, torrent: Dict):
        # we don't want to consider cross-seeded torrents uploaded by the bot
        label = torrent["label".encode("utf-8")].decode("utf-8").lower()

        if self.seed_label.lower() == label:
            return False
        # user wants to ignore labels, hence we'll consider all the torrents
        if self.target_label.lower() == "IGNORE_LABEL":
            return True
        return label == self.target_label.lower()

    @staticmethod
    def __do_key_translation(key: str):
        return deluge_keys_translation[key] if key in deluge_keys_translation else key

    def __extract_necessary_keys(self, torrent: Dict):
        torrent_data = {
            self.__do_key_translation(key): self.__process_torrent_data(torrent, key)
            for key in deluge_keys
        }
        torrent_data["save_path"] = f"{torrent_data['save_path']}/".replace("//", "/")
        torrent_data["content_path"] = (
            f"{torrent_data['save_path']}{torrent_data['name']}"
        )
        return torrent_data

    @staticmethod
    def __process_torrent_data(torrent: Dict, key: str):
        data = torrent[key.encode("utf-8")]
        if isinstance(data, int):
            return data
        if key.lower() == "label":
            return data.decode("utf-8").lower()
        return data.decode("utf-8")
