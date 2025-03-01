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

import sys
from unittest import mock

from auto_upload import GGBotUploadAssistant


class TestGGBotUploadAssistant:
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
    def test_movie_4k_web_dl_hdr10plus(self, e2e_test_working_folder):
        assistant = GGBotUploadAssistant(
            f"{e2e_test_working_folder}/e2e-tests/resources/config-test.env"
        )
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

    @mock.patch.object(
        sys,
        "argv",
        [
            "test.py",
            "-t",
            "TSP",
            "-p",
            "./resources/How.I.Met.Your.Mother.S09.1080p.DSNP.WEB-DL.DDP7.1.H.264-ReleaseGroup",
            "--auto",
            "--debug",
        ],
    )
    def test_tv_1080p_web_dl(self, e2e_test_working_folder):
        assistant = GGBotUploadAssistant(
            f"{e2e_test_working_folder}/e2e-tests/resources/config-test.env"
        )
        assistant.start(
            [
                f"{e2e_test_working_folder}/e2e-tests/resources/How.I.Met.Your.Mother.S09.1080p.DSNP.WEB-DL.DDP7.1.H.264-ReleaseGroup"
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
        assert assistant.torrent_info["title"] == "How I Met Your Mother"
        assert "year" not in assistant.torrent_info
        assert assistant.torrent_info["screen_size"] == "1080p"
        assert assistant.torrent_info["source"] == "Web"
        assert assistant.torrent_info["type"] == "episode"
        assert assistant.torrent_info["release_group"] == "ReleaseGroup"
        assert assistant.torrent_info["s00e00"] == "S09"
        assert assistant.torrent_info["season_number"] == "9"
        assert assistant.torrent_info["episode_number"] == "0"
        assert assistant.torrent_info["complete_season"] == "1"
        assert assistant.torrent_info["individual_episodes"] == "0"
        assert assistant.torrent_info["daily_episodes"] == "0"
        assert (
            assistant.torrent_info["raw_file_name"]
            == "How.I.Met.Your.Mother.S09.1080p.DSNP.WEB-DL.DDP7.1.H.264-ReleaseGroup"
        )
        assert assistant.torrent_info["subtitles"] == []
        assert "hdr" not in assistant.torrent_info
        assert assistant.torrent_info["pymediainfo_video_codec"] == "H.264"
        assert assistant.torrent_info["video_codec"] == "H.264"
        assert assistant.torrent_info["audio_codec"] == "DD+"
        assert assistant.torrent_info["audio_channels"] == "7.1"
        assert assistant.torrent_info["imdb"] == "0460649"
        assert assistant.torrent_info["tmdb"] == "1100"
        assert assistant.torrent_info["tvdb"] == "0"
        assert assistant.torrent_info["mal"] == "0"
        assert assistant.torrent_info["tvmaze"] == "171"
        assert assistant.torrent_info["tmdb_metadata"] is not None
        assert assistant.torrent_info["imdb_metadata"] is not None
        assert assistant.torrent_info["source_type"] == "webdl"
        assert assistant.torrent_info["web_source"] == "DSNP"
        assert assistant.torrent_info["web_source_name"] == "Disney+"
        assert assistant.torrent_info["repack"] is None
        assert assistant.torrent_info["edition"] is None
        assert assistant.torrent_info["scene"] == "false"
        assert assistant.torrent_info["dualaudio"] == ""
        assert assistant.torrent_info["multiaudio"] == ""
        assert assistant.torrent_info["commentary"] is False
        assert assistant.torrent_info["language_str"] == "English"
        assert assistant.torrent_info["language_str_if_foreign"] is None
        assert assistant.torrent_info["container"] == ".mkv"
        assert assistant.torrent_info["bit_depth"] == "8"
        assert assistant.torrent_info["web_type"] == "WEB-DL"
        assert (
            assistant.torrent_info["torrent_title"]
            == "How I Met Your Mother S09 1080p DSNP WEB-DL DD+ 7.1 H.264-ReleaseGroup"
        )
        assert assistant.torrent_info["custom_user_inputs"] == [
            {
                "key": "code_code",
                "title": None,
                "value": "This release is sourced from Disney+",
            }
        ]
        assert assistant.torrent_info["duration"] == "94494"
        assert (
            assistant.torrent_info["shameless_self_promotion"]
            == "Uploaded with ❤ using GG-BOT Upload Assistant"
        )
        assert assistant.torrent_info["imdb_with_tt"] == "tt0460649"
        assert assistant.torrent_info["TSP_upload_status"] is True
        assert assistant.torrent_info["post_processing_complete"] is False
