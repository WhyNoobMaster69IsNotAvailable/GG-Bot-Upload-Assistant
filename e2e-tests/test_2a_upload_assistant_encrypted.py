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

import os
import sys
from pathlib import Path
from unittest import mock

import pytest

from auto_upload import GGBotUploadAssistant


class TestGGBotUploadAssistantWithEncryption:
    """Tests for GGBotUploadAssistant with encrypted configuration."""

    """Set up encryption keys and encrypted config for the test class."""
    working_folder = Path(__file__).resolve().parent
    private_key_path = f"{working_folder}/resources/test_private_key.pem"
    public_key_path = f"{working_folder}/resources/test_public_key.pem"

    @pytest.fixture(autouse=True)
    def setup_encrypted_config(self):
        """Setup temporary config file with proper PRIVATE_KEY_PATH."""
        temp_config_path = (
            f"{self.working_folder}/resources/config-test-encrypted-temp.env"
        )

        with open(
            f"{self.working_folder}/resources/config-test-encrypted.env", "r"
        ) as original_file:
            content = original_file.read()

        updated_content = content.replace(
            "PRIVATE_KEY_PATH=e2e-tests/resources/test_private_key.pem",
            f"PRIVATE_KEY_PATH={self.private_key_path}",
        )

        with open(temp_config_path, "w") as temp_file:
            temp_file.write(updated_content)

        yield temp_config_path

        if os.path.exists(temp_config_path):
            os.remove(temp_config_path)

    @mock.patch.object(
        sys,
        "argv",
        [
            "test.py",
            "-t",
            "TSP",
            "-p",
            "./resources/Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv",
            "--auto",
            "--debug",
        ],
    )
    def test_upload_assistant_with_encrypted_config(
        self, e2e_test_working_folder, setup_encrypted_config
    ):
        """Test upload assistant with encrypted configuration file."""
        # Get the temporary config path from the fixture
        temp_config_path = setup_encrypted_config

        # Use the temporary config file for the test
        assistant = GGBotUploadAssistant(temp_config_path)
        assistant.start(
            [
                f"{e2e_test_working_folder}/e2e-tests/resources/Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv"
            ]
        )

        # assert that api_key_dict is loaded
        assert assistant.api_keys_dict != {}
        # assert that torrent_info is not empty
        assert assistant.torrent_info != {}
        assert assistant.torrent_info["argument_tags"] is None
        # assert that tag_grouping is loaded properly
        assert assistant.torrent_info["tag_grouping"] is not None
        assert assistant.torrent_info["3d"] == "0"
        assert assistant.torrent_info["foregin"] == "0"
        assert assistant.torrent_info["title"] == "Deadpool & Wolverine"
        assert assistant.torrent_info["year"] == "2024"
        assert assistant.torrent_info["screen_size"] == "2160p"
        assert assistant.torrent_info["source"] == "Web"
        assert assistant.torrent_info["type"] == "movie"
        assert assistant.torrent_info["release_group"] == "ReleaseGroup"
        assert (
            assistant.torrent_info["raw_file_name"]
            == "Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv"
        )
        assert assistant.torrent_info["subtitles"] == []
        assert assistant.torrent_info["hdr"] == "HDR10+"
        assert assistant.torrent_info["pymediainfo_video_codec"] == "H.265"
        assert assistant.torrent_info["video_codec"] == "H.264"
        assert assistant.torrent_info["audio_codec"] == "DD+"
        assert assistant.torrent_info["audio_channels"] == "5.1"
        assert assistant.torrent_info["imdb"] == "6263850"
        assert assistant.torrent_info["tmdb"] == "533535"
        assert assistant.torrent_info["tvdb"] == "0"
        assert assistant.torrent_info["mal"] == "0"
        assert assistant.torrent_info["tvmaze"] == "0"
        assert assistant.torrent_info["source_type"] == "webdl"
        assert assistant.torrent_info["web_source"] == "AMZN"
        assert assistant.torrent_info["web_source_name"] == "Amazon Prime"
        assert assistant.torrent_info["repack"] is None
        assert assistant.torrent_info["edition"] is None
        assert assistant.torrent_info["scene"] == "true"  # TODO: this needs to be fixed
        assert assistant.torrent_info["dualaudio"] == ""
        assert assistant.torrent_info["multiaudio"] == ""
        assert assistant.torrent_info["commentary"] is False
        assert assistant.torrent_info["language_str"] == "English"
        assert assistant.torrent_info["language_str_if_foreign"] is None
        assert assistant.torrent_info["container"] == ".mkv"
        assert assistant.torrent_info["bit_depth"] == "10"
        assert assistant.torrent_info["web_type"] == "WEB-DL"
        assert (
            assistant.torrent_info["torrent_title"]
            == "Deadpool & Wolverine 2024 2160p AMZN WEB-DL DD+ 5.1 HDR10+ H.264-ReleaseGroup"
        )
        assert assistant.torrent_info["custom_user_inputs"] == [
            {
                "key": "code_code",
                "title": None,
                "value": "This release is sourced from Amazon Prime",
            }
        ]
        assert assistant.torrent_info["duration"] == "50050"
        assert (
            assistant.torrent_info["shameless_self_promotion"]
            == "Uploaded with ❤ using GG-BOT Upload Assistant"
        )
        assert assistant.torrent_info["imdb_with_tt"] == "tt6263850"
        assert assistant.torrent_info["TSP_upload_status"] is True
        assert assistant.torrent_info["post_processing_complete"] is False
