# GG Bot Upload Assistant
# Copyright (C) 2022  Noob Master669

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
import logging
from typing import Optional

import requests

from modules.config import ClientConfig, ReUploaderConfig
from modules.exceptions.exception import GGBotRetryException
from modules.helpers import retry_on_failure
from modules.torrent_clients.base import GGBotTorrentClientTemplate

rutorrent_keys = [
    "d.get_custom1",
    "d.get_bytes_done",
    "d.get_base_path",
    "hash",
    "d.get_name",
    "d.get_size_bytes",
]
rutorrent_keys_translation = {
    "d.get_custom1": "category",
    "d.get_bytes_done": "completed",
    "d.get_base_path": "content_path",
    "d.get_name": "name",
    "d.get_size_bytes": "size",
}


class Rutorrent(GGBotTorrentClientTemplate):
    __connection_check_path = "/plugins/check_port/action.php?init"
    __cpu_load_path = "/plugins/cpuload/action.php"
    __disk_size_path = "/plugins/diskspace/action.php"
    __default_path = "/plugins/httprpc/action.php"
    __upload_torrent_path = "/php/addtorrent.php"
    __get_plugins_path = "/php/getplugins.php"

    def __init__(self):
        super().__init__()
        self.client_config = ClientConfig()
        self.reuploader_config = ReUploaderConfig()
        self.host = self.client_config.CLIENT_HOST
        if self.host is None or len(self.host) == 0:
            raise Exception("Invalid RuTorrent host provided")

        self.port = self.client_config.CLIENT_PORT
        self.username = self.client_config.CLIENT_USERNAME
        self.password = self.client_config.CLIENT_PASSWORD
        self.path = self.client_config.CLIENT_PATH
        self.base_url = f"{self.host}:{self.port}{self.path}"

        if self.username:
            hashed = base64.b64encode(
                f"{self.username}:{self.password or ''}".encode("ascii")
            ).decode("ascii")
            self.header = {"Authorization": f"Basic {hashed}"}
        else:
            self.header = {}

        self._initialize_reuploader_config(self.reuploader_config)

        try:
            logging.info("[Rutorrent] Checking connection to Rutorrent")
            self.__call_server(f"{self.base_url}{self.__connection_check_path}")
            print("Successfully established connection with Rutorrent")
        except Exception as err:
            logging.fatal("[Rutorrent] Authentication with Rutorrent instance failed")
            raise err

    def hello(self):
        _, response = self.__call_server(f"{self.base_url}{self.__cpu_load_path}")
        try:
            if not isinstance(response, dict):
                raise Exception("Failed to connect to rutorrent instance.")
            print(f"Rutorrent CPU Load: {response['load']}%")
            _, response = self.__call_server(f"{self.base_url}{self.__disk_size_path}")
            print(
                f"Rutorrent Storage: {self.__format_bytes(response['free'])} free out of {self.__format_bytes(response['total'])}"
            )
            # Loading the plugins. This call us needed to ensure that all the plugins are loaded.
            # Open issue in crazymax docker images: https://github.com/crazy-max/docker-rtorrent-rutorrent/issues/247
            self.__call_server(
                f"{self.base_url}{self.__get_plugins_path}", method="GET"
            )
        except Exception as err:
            logging.fatal(f"Failed to connect to rutorrent. Error:{response.text}")
            raise err

    def _list_all_torrents(self):
        status_code, response = self.__call_server(
            f"{self.base_url}{self.__default_path}", data={"mode": "list"}
        )
        if status_code != 200:
            logging.error(f"[RuTorrent] Failed to list torrents. Error : {response}")
            raise GGBotRetryException(response)

        if isinstance(response["t"], list):
            return {}

        return response["t"].items()

    @retry_on_failure()
    def list_all_torrents(self):
        response = self._list_all_torrents()

        return list(
            map(self.__extract_necessary_keys, map(self.__get_torrent_info, response))
        )

    @retry_on_failure()
    def list_torrents(self):
        status_code, response = self.__call_server(
            f"{self.base_url}{self.__default_path}", data={"mode": "list"}
        )
        if status_code != 200:
            logging.error(f"[RuTorrent] Failed to list torrents. Error : {response}")
            raise GGBotRetryException(response)

        if isinstance(response["t"], list):
            return []

        return list(
            map(
                self.__extract_necessary_keys,
                filter(
                    self.__match_label,
                    map(self.__get_torrent_info, response["t"].items()),
                ),
            )
        )

    def upload_torrent(
        self,
        torrent,
        save_path,
        use_auto_torrent_management,
        is_skip_checking,
        category=None,
    ):
        category = category if category is not None else self.seed_label
        logging.info(f"[Rutorrent] Uploading torrent with category {category}")
        status_code, response = self.__call_server(
            f"{self.base_url}{self.__upload_torrent_path}",
            data={
                "fast_resume": "1" if is_skip_checking else "0",
                "label": category,
                "dir_edit": save_path,
            },
            files={"torrent_file": open(torrent, "rb")},
        )
        logging.info(
            f"[Rutorrent] Torrent upload response. Status Code: {status_code} <=> Response: {response}"
        )

    def update_torrent_category(
        self, info_hash: str, category_name: Optional[str] = None
    ) -> None:
        category_name = self.source_label if category_name is None else category_name
        logging.info(
            f"[Rutorrent] Updating category of torrent with hash {info_hash} to {category_name}"
        )
        _, response = self.__call_server(
            f"{self.base_url}{self.__default_path}",
            data={
                "mode": "setlabel",
                "hash": info_hash,
                "v": category_name,
                "s": "label",
            },
        )
        if response[0] == category_name:
            logging.info(
                f"[Rutorrent] Successfully updated category of torrent with hash {info_hash} to {category_name}"
            )
        else:
            logging.error(
                f"[RuTorrent] Failed to update category of torrent with hash {info_hash} to {category_name}"
            )

    def __call_server(self, url, method="POST", data=None, files=None, header=None):
        response = requests.request(
            method,
            url,
            data=data if data is not None else {},
            files=files,
            headers=header or self.header,
        )
        return (
            (response.status_code, response.json())
            if "application/json" in response.headers.get("Content-Type")
            else (response.status_code, response.text)
        )

    @staticmethod
    def __get_torrent_info(item):
        key = item[0]
        data = item[1]
        return {
            "hash": key,
            "d.is_open": data[0],
            "d.is_hash_checking": data[1],
            "d.is_hash_checked": data[2],
            "d.get_state": data[3],
            "d.get_name": data[4],
            "d.get_size_bytes": data[5],
            "d.get_completed_chunks": data[6],
            "d.get_size_chunks": data[7],
            "d.get_bytes_done": data[8],
            "d.get_up_total": data[9],
            "d.get_ratio": data[10],
            "d.get_up_rate": data[11],
            "d.get_down_rate": data[12],
            "d.get_chunk_size": data[13],
            "d.get_custom1": data[14],
            "d.get_peers_accounted": data[15],
            "d.get_peers_not_connected": data[16],
            "d.get_peers_connected": data[17],
            "d.get_peers_complete": data[18],
            "d.get_left_bytes": data[19],
            "d.get_priority": data[20],
            "d.get_state_changed": data[21],
            "d.get_skip_total": data[22],
            "d.get_hashing": data[23],
            "d.get_chunks_hashed": data[24],
            "d.get_base_path": data[25],
            "d.get_creation_date": data[26],
            "d.get_tracker_focus": data[27],
            "d.is_active": data[28],
            "d.get_message": data[29],
            "d.get_custom2": data[30],
            "d.get_free_diskspace": data[31],
            "d.is_private": data[32],
            "d.is_multi_file": data[33],
        }

    def __match_label(self, torrent):
        # we don't want to consider cross-seeded torrents uploaded by the bot
        if self.seed_label == torrent["d.get_custom1"]:
            return False
        # user wants to ignore labels, hence we'll consider all the torrents
        if self.target_label == "IGNORE_LABEL":
            return True
        # if dynamic tracker selection is enabled, then labels will follow the pattern GGBOT::TR1::TR2::TR3
        if self.dynamic_tracker_selection:
            return torrent["d.get_custom1"].startswith(self.target_label)
        else:
            return torrent["d.get_custom1"] == self.target_label

    @staticmethod
    def __do_key_translation(key):
        return (
            rutorrent_keys_translation[key]
            if key in rutorrent_keys_translation
            else key
        )

    def __extract_necessary_keys(self, torrent):
        torrent = {
            self.__do_key_translation(key): value
            for key, value in torrent.items()
            if key in rutorrent_keys
        }
        torrent["save_path"] = torrent["content_path"].replace(torrent["name"], "")
        torrent["category"] = torrent["category"].replace("%3A", ":")
        return torrent

    @staticmethod
    def __format_bytes(size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
        while size > power:
            size /= power
            n += 1
        return f"{int(size)} {power_labels[n]}B"
