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

import glob
import json
import logging
import shutil
from typing import Optional

import requests

from modules.constants import WORKING_DIR


def redownload_torrent_from_json_response(
    torrent_info, _, tracker_config, working_folder
):
    logging.info("[CustomAction][UNIT3D] Torrent redownload requested.")

    tracker = tracker_config["name"]
    tracker_response = torrent_info[f"{tracker}_upload_response"]
    try:
        tracker_response = json.loads(tracker_response)
    except json.JSONDecodeError:
        logging.error(
            f"[CustomAction][UNIT3D] Failed to parse tracker response: {tracker_response}"
        )
        logging.error("[CustomAction][UNIT3D] Not a valid json. Skipping redownload.")
        return

    existing_torrent_file: Optional[str] = find_tracker_torrent_file(
        tracker, working_folder, torrent_info["working_folder"]
    )
    if existing_torrent_file is None:
        logging.error(
            "[CustomAction][UNIT3D] Failed to find torrent file. Skipping redownload."
        )
        return

    download_url = tracker_response["data"]
    logging.info(f"[CustomAction][UNIT3D] Download url: {download_url}")

    logging.info("[CustomAction][UNIT3D] Backing up existing torrent file.")
    try:
        shutil.copyfile(
            existing_torrent_file,
            existing_torrent_file.replace(tracker, f"BKP_{tracker}"),
        )
    except FileNotFoundError:
        logging.error(
            f"[CustomAction][UNIT3D] Failed to backup existing torrent file: {existing_torrent_file}"
        )
        return

    try:
        logging.info("[CustomAction][UNIT3D] Downloading new torrent file.")
        new_torrent_file = requests.get(download_url)
        open(existing_torrent_file, "wb").write(new_torrent_file.content)
        logging.info("[CustomAction][UNIT3D] Torrent redownload successful.")
    except Exception as e:
        logging.error(f"[CustomAction][UNIT3D] Failed to download torrent file: {e}")
        return


def find_tracker_torrent_file(
    tracker: str, working_folder: str, torrent_working_folder: str
) -> Optional[str]:
    for file in glob.glob(
        f"{WORKING_DIR.format(base_path=working_folder)}{torrent_working_folder}"
        + r"/*.torrent"
    ):
        if f"/{tracker}-" in file:
            logging.info(f"[CustomAction][UNIT3D] Identified .torrent file '{file}'")
            return file
    return None
