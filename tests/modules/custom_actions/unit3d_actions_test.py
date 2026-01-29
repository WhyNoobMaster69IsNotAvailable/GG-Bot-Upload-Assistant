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

import json
import os
import pytest

from pathlib import Path

import modules.custom_actions.unit3d_actions as unit3d_actions


working_folder = Path(__file__).resolve().parent.parent.parent.parent
# The WORKING_DIR constant adds "/temp_upload/" to the base path
# So torrent_working_folder should be relative to temp_upload/
torrent_working_folder_name = "unit3d_test"


@pytest.fixture(scope="function")
def prepare_working_folder():
    """Create a temporary working folder with test torrent files.

    The function under test uses WORKING_DIR which is "{base_path}/temp_upload/",
    so we need to create files in temp_upload/ subdirectory.
    """
    # Create the full path: {working_folder}/temp_upload/{torrent_working_folder_name}/
    folder = f"{working_folder}/temp_upload/{torrent_working_folder_name}/"

    if Path(folder).is_dir():
        clean_up(folder)

    # Create the directory structure
    os.makedirs(folder, exist_ok=True)

    # Create test torrent files with the pattern /{tracker}-
    Path(f"{folder}BLU-test_upload.torrent").touch()
    Path(f"{folder}ATH-another_upload.torrent").touch()

    yield folder

    clean_up(folder)


def clean_up(pth):
    pth = Path(pth)
    if pth.exists():
        for child in pth.iterdir():
            if child.is_file():
                child.unlink()
            else:
                clean_up(child)
        pth.rmdir()


class MockResponse:
    """Mock response object for requests.get."""

    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code


# ============================================================================
# Tests for find_tracker_torrent_file
# ============================================================================


class TestFindTrackerTorrentFile:
    def test_find_tracker_torrent_file_returns_matching_file(
        self, prepare_working_folder
    ):
        """Test that the function finds and returns the correct torrent file."""
        result = unit3d_actions.find_tracker_torrent_file(
            tracker="BLU",
            working_folder=str(working_folder),
            torrent_working_folder=torrent_working_folder_name,
        )

        assert result is not None
        assert "/BLU-" in result
        assert result.endswith(".torrent")

    def test_find_tracker_torrent_file_returns_correct_tracker(
        self, prepare_working_folder
    ):
        """Test that the function returns the file for the correct tracker."""
        result = unit3d_actions.find_tracker_torrent_file(
            tracker="ATH",
            working_folder=str(working_folder),
            torrent_working_folder=torrent_working_folder_name,
        )

        assert result is not None
        assert "/ATH-" in result
        assert "/BLU-" not in result

    def test_find_tracker_torrent_file_returns_none_when_no_match(
        self, prepare_working_folder
    ):
        """Test that the function returns None when no matching torrent file exists."""
        result = unit3d_actions.find_tracker_torrent_file(
            tracker="NONEXISTENT",
            working_folder=str(working_folder),
            torrent_working_folder=torrent_working_folder_name,
        )

        assert result is None

    def test_find_tracker_torrent_file_returns_none_for_empty_directory(
        self, prepare_working_folder
    ):
        """Test that the function returns None when directory has no torrent files."""
        # Create an empty subdirectory
        empty_dir = f"{working_folder}/temp_upload/empty_folder"
        os.makedirs(empty_dir, exist_ok=True)

        result = unit3d_actions.find_tracker_torrent_file(
            tracker="BLU",
            working_folder=str(working_folder),
            torrent_working_folder="empty_folder",
        )

        # Clean up the empty folder
        os.rmdir(empty_dir)

        assert result is None

    def test_find_tracker_torrent_file_returns_none_for_nonexistent_directory(self):
        """Test that the function returns None when directory doesn't exist."""
        result = unit3d_actions.find_tracker_torrent_file(
            tracker="BLU",
            working_folder=str(working_folder),
            torrent_working_folder="nonexistent/path/here",
        )

        assert result is None


# ============================================================================
# Tests for redownload_torrent_from_json_response
# ============================================================================


class TestRedownloadTorrentFromJsonResponse:
    def test_redownload_torrent_success(self, prepare_working_folder, mocker):
        """Test successful torrent redownload."""
        tracker_config = {"name": "BLU"}
        torrent_info = {
            "BLU_upload_response": json.dumps(
                {"data": "https://example.com/download/torrent123"}
            ),
            "working_folder": torrent_working_folder_name,
        }

        mock_response = MockResponse(content=b"new torrent content")
        mocker.patch("requests.get", return_value=mock_response)

        unit3d_actions.redownload_torrent_from_json_response(
            torrent_info=torrent_info,
            _=None,
            tracker_config=tracker_config,
            working_folder=str(working_folder),
        )

        # Verify backup file was created
        backup_files = list(Path(prepare_working_folder).glob("BKP_BLU-*.torrent"))
        assert len(backup_files) == 1

        # Verify original file was overwritten with new content
        original_file = f"{prepare_working_folder}BLU-test_upload.torrent"
        with open(original_file, "rb") as f:
            assert f.read() == b"new torrent content"

    def test_redownload_torrent_invalid_json_response(
        self, prepare_working_folder, caplog
    ):
        """Test that invalid JSON response is handled gracefully."""
        tracker_config = {"name": "BLU"}
        torrent_info = {
            "BLU_upload_response": "not valid json",
            "working_folder": torrent_working_folder_name,
        }

        unit3d_actions.redownload_torrent_from_json_response(
            torrent_info=torrent_info,
            _=None,
            tracker_config=tracker_config,
            working_folder=str(working_folder),
        )

        assert "Failed to parse tracker response" in caplog.text
        assert "Not a valid json" in caplog.text

    def test_redownload_torrent_no_torrent_file_found(
        self, prepare_working_folder, caplog
    ):
        """Test handling when torrent file is not found."""
        tracker_config = {"name": "NONEXISTENT"}
        torrent_info = {
            "NONEXISTENT_upload_response": json.dumps(
                {"data": "https://example.com/download/torrent123"}
            ),
            "working_folder": torrent_working_folder_name,
        }

        unit3d_actions.redownload_torrent_from_json_response(
            torrent_info=torrent_info,
            _=None,
            tracker_config=tracker_config,
            working_folder=str(working_folder),
        )

        assert "Failed to find torrent file" in caplog.text

    def test_redownload_torrent_backup_failure(
        self, prepare_working_folder, mocker, caplog
    ):
        """Test handling when backup file creation fails."""
        tracker_config = {"name": "BLU"}
        torrent_info = {
            "BLU_upload_response": json.dumps(
                {"data": "https://example.com/download/torrent123"}
            ),
            "working_folder": torrent_working_folder_name,
        }

        # Mock shutil.copyfile to raise FileNotFoundError
        mocker.patch("shutil.copyfile", side_effect=FileNotFoundError("File not found"))

        unit3d_actions.redownload_torrent_from_json_response(
            torrent_info=torrent_info,
            _=None,
            tracker_config=tracker_config,
            working_folder=str(working_folder),
        )

        assert "Failed to backup existing torrent file" in caplog.text

    def test_redownload_torrent_download_failure(
        self, prepare_working_folder, mocker, caplog
    ):
        """Test handling when download fails."""
        tracker_config = {"name": "BLU"}
        torrent_info = {
            "BLU_upload_response": json.dumps(
                {"data": "https://example.com/download/torrent123"}
            ),
            "working_folder": torrent_working_folder_name,
        }

        # Mock requests.get to raise an exception
        mocker.patch("requests.get", side_effect=Exception("Connection error"))

        unit3d_actions.redownload_torrent_from_json_response(
            torrent_info=torrent_info,
            _=None,
            tracker_config=tracker_config,
            working_folder=str(working_folder),
        )

        assert "Failed to download torrent file" in caplog.text

    def test_redownload_torrent_logs_download_url(
        self, prepare_working_folder, mocker, caplog
    ):
        """Test that the download URL is logged."""
        import logging

        caplog.set_level(logging.INFO)

        tracker_config = {"name": "BLU"}
        download_url = "https://example.com/download/torrent123"
        torrent_info = {
            "BLU_upload_response": json.dumps({"data": download_url}),
            "working_folder": torrent_working_folder_name,
        }

        mock_response = MockResponse(content=b"new torrent content")
        mocker.patch("requests.get", return_value=mock_response)

        unit3d_actions.redownload_torrent_from_json_response(
            torrent_info=torrent_info,
            _=None,
            tracker_config=tracker_config,
            working_folder=str(working_folder),
        )

        assert download_url in caplog.text

    def test_redownload_torrent_with_different_trackers(
        self, prepare_working_folder, mocker
    ):
        """Test redownload works correctly with different tracker names."""
        tracker_config = {"name": "ATH"}
        torrent_info = {
            "ATH_upload_response": json.dumps(
                {"data": "https://example.com/download/ath_torrent"}
            ),
            "working_folder": torrent_working_folder_name,
        }

        mock_response = MockResponse(content=b"ath torrent content")
        mocker.patch("requests.get", return_value=mock_response)

        unit3d_actions.redownload_torrent_from_json_response(
            torrent_info=torrent_info,
            _=None,
            tracker_config=tracker_config,
            working_folder=str(working_folder),
        )

        # Verify backup file was created for ATH
        backup_files = list(Path(prepare_working_folder).glob("BKP_ATH-*.torrent"))
        assert len(backup_files) == 1

        # Verify ATH file was overwritten
        ath_file = f"{prepare_working_folder}ATH-another_upload.torrent"
        with open(ath_file, "rb") as f:
            assert f.read() == b"ath torrent content"
