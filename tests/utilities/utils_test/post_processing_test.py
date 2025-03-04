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

from pathlib import Path

from utilities.utils import GenericUtils

working_folder = Path(__file__).resolve().parent.parent.parent.parent


def test_get_torrent_client_for_cross_seeding(mocker):
    mock_client = mocker.patch("modules.torrent_client.TorrentClient")
    mocker.patch(
        "modules.torrent_client.TorrentClientFactory.create",
        return_value=mock_client,
    )
    mocker.patch("os.getenv", side_effect=__post_processing_cross_seed)
    assert GenericUtils.get_torrent_client_if_needed() == mock_client


def test_get_torrent_client_for_no_post_processing(mocker):
    mocker.patch("os.getenv", side_effect=__post_processing_no_post_processing)
    assert GenericUtils.get_torrent_client_if_needed() is None


def test_get_torrent_client_for_watch_folder(mocker):
    mocker.patch("os.getenv", side_effect=__post_processing_watch_folder)
    assert GenericUtils.get_torrent_client_if_needed() is None


def test_client_upload_movie_folder_with_translation_sad_path(mocker):
    torrent_info = {}
    torrent_info["raw_file_name"] = (
        "Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA"
    )
    torrent_info["raw_video_file"] = (
        "/gg-bot-upload-assistant/files/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA.mkv"
    )
    torrent_info["upload_media"] = (
        "/gg-bot-upload-assistant/files/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA/"
    )
    torrent_info["TRACKER_upload_status"] = True
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "test_working_folder/"
    tracker = "TRACKER"

    mocker.patch(
        "os.getenv",
        side_effect=__cross_seed_with_translation_side_effect_sad_path,
    )
    mock_client = mocker.patch("modules.torrent_client.TorrentClient")
    assert (
        GenericUtils().perform_post_processing(
            torrent_info, mock_client, working_folder, tracker
        )
        is False
    )


def test_invalid_processing_mode(mocker):
    torrent_info = {}
    torrent_info["raw_file_name"] = (
        "Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA"
    )
    torrent_info["raw_video_file"] = (
        "/gg-bot-upload-assistant/files/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA.mkv"
    )
    torrent_info["upload_media"] = (
        "/gg-bot-upload-assistant/files/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA/"
    )
    torrent_info["TRACKER_upload_status"] = True
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "test_working_folder/"
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__invalid_processing_mode_side_effect)
    mock_client = mocker.patch("modules.torrent_client.TorrentClient")
    assert (
        GenericUtils().perform_post_processing(
            torrent_info, mock_client, working_folder, tracker
        )
        is False
    )


def test_no_client_upload(mocker):
    torrent_info = {}
    torrent_info["raw_file_name"] = (
        "Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA"
    )
    torrent_info["raw_video_file"] = (
        "/gg-bot-upload-assistant/files/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA.mkv"
    )
    torrent_info["upload_media"] = (
        "/gg-bot-upload-assistant/files/Varathan.2018.1080p.Blu-ray.Remux.AVC.DTS-HD.MA.5.1-FAFDA/"
    )
    torrent_info["TRACKER_upload_status"] = True
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "test_working_folder/"
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__no_cross_seed_side_effect)
    mock_client = mocker.patch("modules.torrent_client.TorrentClient")
    assert (
        GenericUtils().perform_post_processing(
            torrent_info, mock_client, working_folder, tracker
        )
        is False
    )


def __cross_seed_with_translation_side_effect_sad_path(param, default):
    if param in ["enable_post_processing", "translation_needed"]:
        return True
    elif param == "post_processing_mode":
        return "CROSS_SEED"
    else:
        return default


def __no_cross_seed_side_effect(param, default):
    return default


def __invalid_processing_mode_side_effect(param, default):
    if param == "enable_post_processing":
        return True
    elif param == "post_processing_mode":
        return "foo_bar"
    return default


def __post_processing_cross_seed(param, default=None):
    if param == "enable_post_processing":
        return "True"
    elif param == "post_processing_mode":
        return "CROSS_SEED"
    elif param == "client":
        return "Rutorrent"
    else:
        return None


def __post_processing_watch_folder(param, default=None):
    if param == "enable_post_processing":
        return "True"
    elif param == "post_processing_mode":
        return "WATCH_FOLDER"
    return None


def __post_processing_no_post_processing(param, default=None):
    if param == "enable_post_processing":
        return "False"
    return None
