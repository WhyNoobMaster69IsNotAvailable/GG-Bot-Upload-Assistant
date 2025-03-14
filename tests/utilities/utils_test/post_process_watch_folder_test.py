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

import pytest

from pathlib import Path

from utilities.utils import GenericUtils

working_folder = Path(__file__).resolve().parent.parent.parent.parent
temp_working_dir = "/tests/working_folder"


def touch(file_path):
    fp = open(file_path, "x")
    fp.close()


def clean_up(pth):
    pth = Path(pth)
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            clean_up(child)
    pth.rmdir()


@pytest.fixture(scope="function", autouse=True)
def run_around_tests():
    folder = f"{working_folder}{temp_working_dir}"

    if Path(folder).is_dir():
        clean_up(folder)

    Path(f"{folder}/torrent/").mkdir(parents=True, exist_ok=True)  # torrents folder
    Path(f"{folder}/media").mkdir(parents=True, exist_ok=True)  # media folder
    Path(f"{folder}/move/torrent").mkdir(parents=True, exist_ok=True)  # media folder
    Path(f"{folder}/move/media").mkdir(parents=True, exist_ok=True)  # media folder

    touch(f"{folder}/media/file.mkv")
    touch(f"{folder}/torrent/test1.torrent")
    touch(f"{folder}/torrent/test2.torrent")
    yield
    clean_up(folder)


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------ Tests For Watch Folder ------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def __watch_folder_no_type_side_effect(param, default=None):
    if param == "enable_post_processing":
        return True
    elif param == "translation_needed":
        return False
    elif param == "dot_torrent_move_location":
        return f"{working_folder}{temp_working_dir}/move/torrent"
    elif param == "media_move_location":
        return f"{working_folder}{temp_working_dir}/move/media"
    elif param == "post_processing_mode":
        return "WATCH_FOLDER"
    else:
        return default


# moving media with type based movement


def __watch_folder_media_type_side_effect(param, default=None):
    if param == "dot_torrent_move_location":
        return ""
    else:
        return __watch_folder_type_side_effect(param, default)


# moving media


def __watch_folder_media_no_type_side_effect(param, default=None):
    if param == "dot_torrent_move_location":
        return ""
    else:
        return __watch_folder_no_type_side_effect(param, default)


# moving torrent with type based movement


def __watch_folder_torrent_type_side_effect(param, default=None):
    if param == "media_move_location":
        return ""
    else:
        return __watch_folder_type_side_effect(param, default)


# moving torrent


def __watch_folder_torrent_no_type_side_effect(param, default=None):
    if param == "media_move_location":
        return ""
    else:
        return __watch_folder_no_type_side_effect(param, default)


def __watch_folder_type_side_effect(param, default=None):
    if param == "enable_type_base_move":
        return True
    else:
        return __watch_folder_no_type_side_effect(param, default)


"""
    Cases for WATCH_FOLDER
    1. Move media and torrent
    2. Move media and torrent with type based movement
    3. Move media
    4. Move media with type based movement
    5. Move torrent
    6. Move torrent with type based movement
"""


# moving torrent and media


def test_watch_folder_torrent_media(mocker):
    torrent_info = {}
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "WORKING_FOLDER"
    torrent_info["upload_media"] = "tests/working_folder/media/file.mkv"
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__watch_folder_no_type_side_effect)
    mocker.patch(
        "glob.glob",
        return_value=[
            f"{working_folder}{temp_working_dir}/torrent/test1.torrent",
            f"{working_folder}{temp_working_dir}/torrent/test2.torrent",
        ],
    )

    GenericUtils().perform_post_processing(torrent_info, None, working_folder, tracker)

    moved_media_path = Path(f"{working_folder}{temp_working_dir}/move/media/file.mkv")
    moved_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test1.torrent"
    )
    moved_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test2.torrent"
    )

    original_media_path = Path(f"{working_folder}{temp_working_dir}/media/file.mkv")
    original_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test1.torrent"
    )
    original_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test2.torrent"
    )

    assert original_media_path.is_file() is False
    assert original_torrent_1_path.is_file() is False
    assert original_torrent_2_path.is_file() is False

    assert moved_media_path.is_file() is True
    assert moved_torrent_1_path.is_file() is True
    assert moved_torrent_2_path.is_file() is True


# moving torrent and media with type based movement
def test_watch_folder_torrent_media_type(mocker):
    torrent_info = {}
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "WORKING_FOLDER"
    torrent_info["upload_media"] = "tests/working_folder/media/file.mkv"
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__watch_folder_type_side_effect)
    mocker.patch(
        "glob.glob",
        return_value=[
            f"{working_folder}{temp_working_dir}/torrent/test1.torrent",
            f"{working_folder}{temp_working_dir}/torrent/test2.torrent",
        ],
    )

    GenericUtils().perform_post_processing(torrent_info, None, working_folder, tracker)

    moved_media_path = Path(
        f"{working_folder}{temp_working_dir}/move/media/movie/file.mkv"
    )
    moved_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/movie/test1.torrent"
    )
    moved_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/movie/test2.torrent"
    )

    original_media_path = Path(f"{working_folder}{temp_working_dir}/media/file.mkv")
    original_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test1.torrent"
    )
    original_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test2.torrent"
    )

    assert original_media_path.is_file() is False
    assert original_torrent_1_path.is_file() is False
    assert original_torrent_2_path.is_file() is False

    assert moved_torrent_1_path.is_file() is True
    assert moved_torrent_2_path.is_file() is True
    assert moved_media_path.is_file() is True


# moving torrent


def test_watch_folder_torrent(mocker):
    torrent_info = {}
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "WORKING_FOLDER"
    torrent_info["upload_media"] = "tests/working_folder/media/file.mkv"
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__watch_folder_torrent_no_type_side_effect)
    mocker.patch(
        "glob.glob",
        return_value=[
            f"{working_folder}{temp_working_dir}/torrent/test1.torrent",
            f"{working_folder}{temp_working_dir}/torrent/test2.torrent",
        ],
    )

    GenericUtils().perform_post_processing(torrent_info, None, working_folder, tracker)

    moved_media_path = Path(f"{working_folder}{temp_working_dir}/move/media/file.mkv")
    moved_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test1.torrent"
    )
    moved_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test2.torrent"
    )

    original_media_path = Path(f"{working_folder}{temp_working_dir}/media/file.mkv")
    original_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test1.torrent"
    )
    original_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test2.torrent"
    )

    assert original_media_path.is_file() is True
    assert original_torrent_1_path.is_file() is False
    assert original_torrent_2_path.is_file() is False

    assert moved_media_path.is_file() is False
    assert moved_torrent_1_path.is_file() is True
    assert moved_torrent_2_path.is_file() is True


# moving torrent with type based movement


def test_watch_folder_torrent_relative_input_type_happy(mocker):
    torrent_info = {}
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "WORKING_FOLDER"
    torrent_info["upload_media"] = "tests/working_folder/media/file.mkv"
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__watch_folder_torrent_type_side_effect)
    mocker.patch(
        "glob.glob",
        return_value=[
            f"{working_folder}{temp_working_dir}/torrent/test1.torrent",
            f"{working_folder}{temp_working_dir}/torrent/test2.torrent",
        ],
    )

    GenericUtils().perform_post_processing(torrent_info, None, working_folder, tracker)

    moved_media_path = Path(f"{working_folder}{temp_working_dir}/move/media/file.mkv")
    moved_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/movie/test1.torrent"
    )
    moved_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/movie/test2.torrent"
    )

    original_media_path = Path(f"{working_folder}{temp_working_dir}/media/file.mkv")
    original_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test1.torrent"
    )
    original_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test2.torrent"
    )

    assert original_media_path.is_file() is True
    assert original_torrent_1_path.is_file() is False
    assert original_torrent_2_path.is_file() is False

    assert moved_media_path.is_file() is False
    assert moved_torrent_1_path.is_file() is True
    assert moved_torrent_2_path.is_file() is True


# moving media


def test_watch_folder_torrent_1(mocker):
    torrent_info = {}
    torrent_info["type"] = "movie"
    torrent_info["working_folder"] = "WORKING_FOLDER"
    torrent_info["upload_media"] = "tests/working_folder/media/file.mkv"
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__watch_folder_media_no_type_side_effect)
    mocker.patch(
        "glob.glob",
        return_value=[
            f"{working_folder}{temp_working_dir}/torrent/test1.torrent",
            f"{working_folder}{temp_working_dir}/torrent/test2.torrent",
        ],
    )

    GenericUtils().perform_post_processing(torrent_info, None, working_folder, tracker)

    moved_media_path = Path(f"{working_folder}{temp_working_dir}/move/media/file.mkv")
    moved_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test1.torrent"
    )
    moved_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test2.torrent"
    )

    original_media_path = Path(f"{working_folder}{temp_working_dir}/media/file.mkv")
    original_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test1.torrent"
    )
    original_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test2.torrent"
    )

    assert original_media_path.is_file() is False
    assert original_torrent_1_path.is_file() is True
    assert original_torrent_2_path.is_file() is True

    assert moved_media_path.is_file() is True
    assert moved_torrent_1_path.is_file() is False
    assert moved_torrent_2_path.is_file() is False


# moving media with type based movement


def test_watch_folder_torrent_relative_input_type_happy_1(mocker):
    torrent_info = {
        "type": "movie",
        "working_folder": "WORKING_FOLDER",
        "upload_media": "tests/working_folder/media/file.mkv",
    }
    tracker = "TRACKER"

    mocker.patch("os.getenv", side_effect=__watch_folder_media_type_side_effect)
    mocker.patch(
        "glob.glob",
        return_value=[
            f"{working_folder}{temp_working_dir}/torrent/test1.torrent",
            f"{working_folder}{temp_working_dir}/torrent/test2.torrent",
        ],
    )

    GenericUtils().perform_post_processing(torrent_info, None, working_folder, tracker)

    moved_media_path = Path(
        f"{working_folder}{temp_working_dir}/move/media/movie/file.mkv"
    )
    moved_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test1.torrent"
    )
    moved_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/move/torrent/test2.torrent"
    )

    original_media_path = Path(f"{working_folder}{temp_working_dir}/media/file.mkv")
    original_torrent_1_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test1.torrent"
    )
    original_torrent_2_path = Path(
        f"{working_folder}{temp_working_dir}/torrent/test2.torrent"
    )

    assert original_media_path.is_file() is False
    assert original_torrent_1_path.is_file() is True
    assert original_torrent_2_path.is_file() is True

    assert moved_media_path.is_file() is True
    assert moved_torrent_1_path.is_file() is False
    assert moved_torrent_2_path.is_file() is False
