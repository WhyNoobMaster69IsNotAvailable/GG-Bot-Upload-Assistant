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

from modules.config import TrackerConfig
import logging


def add_announce_pid_to_payload(torrent_info, tracker_settings, tracker_config):
    logging.info("[CustomActions][TL] Adding announcekey to tracker payload")
    tracker_settings["announcekey"] = TrackerConfig("TL").API_KEY


def check_successful_upload(response):
    response_text = response.text

    if response_text.isnumeric():
        logging.info("[CustomActions][TL] Upload to tracker 'SUCCESSFUL'")
        return True, "Successfully Uploaded to TL"
    else:
        logging.info("[CustomActions][TL] Upload to tracker 'FAILED'")
        return False, response_text
