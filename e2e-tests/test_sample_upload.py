import os
import sys
from unittest import mock

import pytest
from auto_upload import GGBotUploadAssistant


class TestGGBotUploadAssistant:
    @pytest.fixture(scope="class", autouse=True)
    def test_with_patched_library_path(self):
        lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "libs"))

        with mock.patch("pymediainfo.MediaInfo._get_library_paths") as mock_get_paths:
            if sys.platform == "darwin":
                mock_get_paths.return_value = (
                    os.path.join(lib_dir, "libmediainfo.0.dylib"),
                    os.path.join(lib_dir, "libmediainfo.dylib"),
                )
            else:
                mock_get_paths.return_value = ("libmediainfo.so.0",)
            yield

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
        ],
    )
    def test_upload(self, working_folder):
        filename = f"{working_folder}/e2e-tests/resources/Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv"
        assert os.path.exists(filename) is True

        assistant = GGBotUploadAssistant(
            f"{working_folder}/e2e-tests/resources/config-test.env"
        )
        assistant.start([filename])

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
