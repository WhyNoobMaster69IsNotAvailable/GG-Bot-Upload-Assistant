# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import json
import shutil
import sys
from pathlib import Path
from unittest import mock

import pytest
from pymongo import MongoClient

from auto_reupload import GGBotReUploader

working_folder = Path(__file__).resolve().parent.parent
temp_working_dir = "/e2e-tests/working_folder"
temp_config_dir = "/temp_config"


def clean_up(pth):
    pth = Path(pth)
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            clean_up(child)
    pth.rmdir()


class TestAutoReuploaderRuTorrent:
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        folder = f"{working_folder}{temp_working_dir}"

        if Path(folder).is_dir():
            clean_up(folder)

        Path(f"{folder}{temp_config_dir}").mkdir(parents=True, exist_ok=True)

        shutil.copy(
            f"{working_folder}/e2e-tests/resources/reupload-test.config.env",
            f"{folder}{temp_config_dir}/reupload-test.config.env",
        )

        yield

        clean_up(folder)

    @pytest.fixture
    def setup_reuploader_env_with_dynamic_config(
        self, mongo_container, rutorrent_credentials, run_around_tests
    ):
        mongo_ip = mongo_container.get_container_host_ip()
        mongo_port = mongo_container.get_exposed_port(27017)

        with open(
            f"{working_folder}{temp_working_dir}{temp_config_dir}/reupload-test.config.env",
            "r",
        ) as config_file:
            config_data = config_file.read()
            config_data = config_data.replace("<<MONGO_HOST_PLACEHOLDER>>", mongo_ip)
            config_data = config_data.replace("<<MONGO_PORT_PLACEHOLDER>>", mongo_port)

            config_data = config_data.replace(
                "<<CLIENT_HOST_PLACEHOLDER>>", f"http://{rutorrent_credentials['host']}"
            )
            config_data = config_data.replace(
                "<<CLIENT_PORT_PLACEHOLDER>>", rutorrent_credentials["port"]
            )

        with open(
            f"{working_folder}{temp_working_dir}{temp_config_dir}/reupload-test.config.env",
            "w",
        ) as config_file:
            config_file.write(config_data)

        yield

    @mock.patch.object(
        sys,
        "argv",
        ["test.py", "-t", "TSP", "PTP", "BLU", "GPW", "--debug"],
    )
    def test_reuploader_setup(
        self, e2e_test_working_folder, setup_reuploader_env_with_dynamic_config
    ):
        reuploader: GGBotReUploader = GGBotReUploader(
            f"{working_folder}{temp_working_dir}{temp_config_dir}/reupload-test.config.env"
        )
        reuploader._run()

        assert reuploader.cache is not None
        assert reuploader.torrent_client is not None
        assert reuploader.reupload_manager is not None
        assert reuploader.working_folder is not None
        assert reuploader.cookies_dump is not None
        assert reuploader.torrent_info is not None
        assert reuploader.torrent_info == {}
        assert reuploader.site_templates_path is not None
        assert reuploader.acronym_to_tracker is not None
        assert reuploader.auto_mode is not None
        assert reuploader.auto_mode == "true"
        assert reuploader.args is not None
        assert reuploader.api_keys_dict is not None
        assert reuploader.reuploader_config is not None
        assert reuploader.template_validator is not None
        assert reuploader.valid_templates is not None
        assert reuploader.upload_to_trackers is not None
        assert reuploader.upload_to_trackers == ["TSP"]
        assert reuploader.server is not None

        mongo_client: MongoClient = reuploader.cache.cache_client.mongo_client
        assert mongo_client is not None

        gg_bot_database = "gg-bot-reuploader"
        expected_collections = [
            "MetaData_TMDB",
            "ReUpload_Torrent",
            "ReUpload_JobRepository",
        ]
        all_databases = list(mongo_client.list_database_names())
        assert gg_bot_database in all_databases

        database = mongo_client.get_database(gg_bot_database)
        assert database is not None

        all_collections = list(database.list_collection_names())
        assert all(collection in all_collections for collection in expected_collections)

    @mock.patch.object(
        sys,
        "argv",
        ["test.py", "-t", "TSP", "PTP", "BLU", "GPW", "--debug"],
    )
    def test_reuploader_with_torrents(
        self, e2e_test_working_folder, setup_reuploader_env_with_dynamic_config
    ):
        reuploader: GGBotReUploader = GGBotReUploader(
            f"{working_folder}{temp_working_dir}{temp_config_dir}/reupload-test.config.env"
        )

        assert reuploader.cache is not None
        assert reuploader.torrent_client is not None
        assert reuploader.reupload_manager is not None
        assert reuploader.working_folder is not None
        assert reuploader.cookies_dump is not None
        assert reuploader.torrent_info is not None
        assert reuploader.torrent_info == {}
        assert reuploader.site_templates_path is not None
        assert reuploader.acronym_to_tracker is not None
        assert reuploader.auto_mode is not None
        assert reuploader.auto_mode == "true"
        assert reuploader.args is not None
        assert reuploader.api_keys_dict is not None
        assert reuploader.reuploader_config is not None
        assert reuploader.template_validator is not None
        assert reuploader.valid_templates is not None
        assert reuploader.upload_to_trackers is not None
        assert reuploader.upload_to_trackers == ["TSP"]
        assert reuploader.server is not None

        reuploader.torrent_client.upload_torrent(
            torrent=f"{working_folder}/e2e-tests/resources/Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv.torrent",
            save_path=f"{working_folder}/e2e-tests/resources/",
            use_auto_torrent_management=False,
            is_skip_checking=False,
            category="GGBOT",
        )

        reuploader._run()
        """
         A successful re-upload will have the following in Mongo Cache
             - MetaData_TMDB: One entry for the upload with title, year, type and all database ids filled
             - ReUpload_Torrent: One entry for the torrent identified from torrent client
             - ReUpload_JobRepository: It'll have entries for all tracker upload jobs. If the torrent needs to be
                re-uploaded to multiple tracker, then for each tracker there will be one document.
        We also need to list all torrents from torrent client and ensure that the new torrent is seeding
            and the original torrent has been moved to a different category.
        """
        gg_bot_database = "gg-bot-reuploader"
        mongo_client: MongoClient = reuploader.cache.cache_client.mongo_client
        database = mongo_client.get_database(gg_bot_database)

        metadata_collection = database.get_collection("MetaData_TMDB")
        documents = list(metadata_collection.find({}))
        expected_movie_db_data = {
            "tmdb": "533535",
            "imdb": "tt6263850",
            "tvmaze": "0",
            "tvdb": "0",
            "mal": "0",
            "title": "Deadpool & Wolverine",
            "year": "2024",
            "type": "movie",
        }
        assert len(documents) == 1
        assert documents[0]["tmdb"] == expected_movie_db_data["tmdb"]
        assert documents[0]["imdb"] == expected_movie_db_data["imdb"]
        assert documents[0]["tvmaze"] == expected_movie_db_data["tvmaze"]
        assert documents[0]["tvdb"] == expected_movie_db_data["tvdb"]
        assert documents[0]["mal"] == expected_movie_db_data["mal"]
        assert documents[0]["title"] == expected_movie_db_data["title"]
        assert documents[0]["year"] == expected_movie_db_data["year"]
        assert documents[0]["type"] == expected_movie_db_data["type"]

        torrent_collection = database.get_collection("ReUpload_Torrent")
        torrents = list(torrent_collection.find({}))
        assert len(torrents) == 1
        assert torrents[0]["hash"] == "F97062F80387BBBD8C1D2F04DBD3830D0706FF80"
        assert (
            torrents[0]["name"]
            == "Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv"
        )
        assert torrents[0]["status"] == "SUCCESS"
        assert torrents[0]["upload_attempt"] == 1
        assert torrents[0]["possible_matches"] == "None"
        assert torrents[0]["torrent"] is not None
        assert "F97062F80387BBBD8C1D2F04DBD3830D0706FF80" in torrents[0]["torrent"]
        assert torrents[0]["movie_db"] is not None
        assert torrents[0]["movie_db"] == json.dumps(expected_movie_db_data)
        assert torrents[0]["id"] is not None

        job_collection = database.get_collection("ReUpload_JobRepository")
        jobs = list(job_collection.find({}))
        assert len(jobs) == 1
        assert jobs[0]["hash"] == "F97062F80387BBBD8C1D2F04DBD3830D0706FF80"
        assert jobs[0]["tracker"] == "TSP"
        assert jobs[0]["status"] == "SUCCESS"
        assert jobs[0]["job_id"] is not None
        assert jobs[0]["tracker_response"] == (
            '{"success": true, "status_code": 0, "data": [], "status_message": '
            '"Successfully uploaded torrent"}'
        )

        all_torrents = reuploader.torrent_client.list_all_torrents()
        assert len(all_torrents) == 2
        for torrent in all_torrents:
            if torrent["hash"] == "F97062F80387BBBD8C1D2F04DBD3830D0706FF80":
                assert torrent["category"] == "GGBotCrossSeed_Source"
            if torrent["hash"] == "607AFF625031CD1F68A8B9C62B044112945F6C9A":
                assert torrent["category"] == "GGBotCrossSeed"

        assert all_torrents[0]["size"] == all_torrents[0]["size"]
        assert all_torrents[0]["completed"] == all_torrents[0]["completed"]
        assert all_torrents[0]["content_path"] == all_torrents[0]["content_path"]
        assert all_torrents[0]["save_path"] == all_torrents[0]["save_path"]

        # torrent_info assertions
        torrent_info = reuploader.torrent_info
        assert torrent_info is not None
        assert torrent_info["argument_tags"] is None
        assert torrent_info["working_folder"] is not None
        # assert torrent_info["working_folder"] == GenericUtils.get_hash("Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv")
        assert torrent_info["cookies_dump"] == f"{working_folder}/cookies/"
        assert torrent_info["base_working_folder"] == str(working_folder)
        # assert torrent_info["absolute_working_folder"] == f"{working_folder}/temp_upload/{GenericUtils.get_hash('Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv')}"
        assert torrent_info["title"] == "Deadpool & Wolverine"
        assert torrent_info["year"] == "2024"
        assert torrent_info["screen_size"] == "2160p"
        assert torrent_info["source"] == "Web"
        assert torrent_info["audio_channels"] == "5.1"
        assert torrent_info["type"] == "movie"
        assert torrent_info["hdr"] == "HDR10+"
        assert torrent_info["pymediainfo_video_codec"] == "H.265"
        assert torrent_info["video_codec"] == "H.264"  # TODO: Fix this
        assert torrent_info["audio_codec"] == "DD+"
        assert torrent_info["release_group"] == "ReleaseGroup"
        assert (
            torrent_info["raw_file_name"]
            == "Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv"
        )
        assert torrent_info["mediainfo_summary"] is not None
        assert torrent_info["mediainfo_summary_data"] is not None
        assert torrent_info["subtitles"] is not None
        assert len(torrent_info["subtitles"]) == 0
        assert torrent_info["imdb"] == "6263850"
        assert torrent_info["imdb_with_tt"] == "tt6263850"
        assert torrent_info["tmdb"] == "533535"
        assert torrent_info["tvdb"] == "0"
        assert torrent_info["mal"] == "0"
        assert torrent_info["tvmaze"] == "0"
        assert torrent_info["tmdb_metadata"] is not None
        assert torrent_info["imdb_metadata"] is not None
        assert torrent_info["source_type"] == "webdl"
        assert torrent_info["web_source"] == "AMZN"
        assert torrent_info["web_source_name"] == "Amazon Prime"
        assert torrent_info["repack"] is None
        assert torrent_info["edition"] is None
        assert (
            torrent_info["scene"] == "true"
        )  # TODO: check whether this needs to be patched
        assert torrent_info["dualaudio"] == ""
        assert torrent_info["multiaudio"] == ""
        assert torrent_info["commentary"] is False
        assert torrent_info["language_str"] == "English"
        assert torrent_info["language_str_if_foreign"] is None
        assert torrent_info["container"] == ".mkv"
        assert torrent_info["bit_depth"] == "10"
        assert torrent_info["web_type"] == "WEB-DL"
        assert (
            torrent_info["torrent_title"]
            == "Deadpool & Wolverine 2024 2160p AMZN WEB-DL DD+ 5.1 HDR10+ H.264-ReleaseGroup"
        )
        assert torrent_info["duration"] == "50050"
