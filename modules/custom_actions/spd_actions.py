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
import logging
import shutil

from torf import Torrent

from modules.constants import WORKING_DIR


def update_torrent_info_hash(torrent_info, _, __, working_folder):
    logging.info("[CustomAction][SPD] Updating torrent info hash")

    torrent_file = None
    for file in glob.glob(
        f"{WORKING_DIR.format(base_path=working_folder)}{torrent_info['working_folder']}"
        + r"/*.torrent"
    ):
        if "/SPD-" in file:
            torrent_file = file
            logging.info(
                f"[CustomAction][SPD] Identified .torrent file '{torrent_file}'"
            )
            break
    if torrent_file is None:
        logging.error(
            "[CustomAction][SPD] Failed to identify the torrent file for SPD. Skipping success processor actions"
        )
        return

    torrent = Torrent.read(torrent_file)
    torrent.metainfo["info"]["source"] = (
        f'{torrent.metainfo["info"]["source"]}-{torrent.infohash}'
    )
    shutil.copyfile(torrent_file, torrent_file.replace("SPD", "BKP_SPD"))

    Torrent.copy(torrent).write(
        filepath=torrent_file,
        overwrite=True,
    )
