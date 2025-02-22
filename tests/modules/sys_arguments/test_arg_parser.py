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


import pytest

from modules.sys_arguments.arg_config import GGBotArgumentConfig
from modules.sys_arguments.arg_entry import GGBotArgumentEntry
from modules.sys_arguments.arg_type import GGBotArgumentType
from tests.modules.sys_arguments.conftest import (
    create_gg_bot_argument_parser_and_perform_assertions,
)


class TestGGBotArgumentParser:
    @pytest.fixture
    def argument_config_upload_assistant(self):
        argument_config = GGBotArgumentConfig(
            name="GG-BOT Upload Assistant",
            description="A powerful automation tool for uploading and re-uploading torrents with metadata generation, screenshot handling, and cross-seeding support.",
            epilog="Supports multiple trackers and clients. Ensure configuration files are set up correctly before use. For more details, visit the official repository.",
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-p",
                option_strings="--path",
                nargs="*",
                help_string="Use this to provide path(s) to file/folder",
            ),
            GGBotArgumentType.REQUIRED,
        )

        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-t",
                option_strings="--trackers",
                nargs="*",
                help_string="Tracker(s) to upload to. Space-separates if multiple (no commas)",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-a",
                option_strings="--all_trackers",
                action="store_true",
                help_string="Select all trackers that can be uploaded to",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-tmdb",
                nargs=1,
                help_string="Use this to manually provide the TMDB ID",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-imdb",
                nargs=1,
                help_string="Use this to manually provide the IMDB ID",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-tvmaze",
                nargs=1,
                help_string="Use this to manually provide the TVMaze ID",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-tvdb",
                nargs=1,
                help_string="Use this to manually provide the TVDB ID",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-mal",
                nargs=1,
                help_string="Use this to manually provide the MAL ID. If uploader detects any MAL id during search, this will be ignored.",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-anon",
                action="store_true",
                help_string="Tf you want your upload to be anonymous (no other info needed, just input '-anon'",
            ),
            GGBotArgumentType.COMMON,
        )

        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-title", nargs=1, help_string="Custom title provided by the user"
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-rg",
                option_strings="--release_group",
                nargs=1,
                help_string="Set the release group for an upload",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-type",
                nargs=1,
                help_string="Use to manually specify 'movie' or 'tv'",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-reupload",
                nargs="*",
                help_string="This is used in conjunction with autodl to automatically re-upload any filter matches",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-batch",
                action="store_true",
                help_string="Pass this arg if you want to upload all the files/folder within the folder you specify with the '-p' arg",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-e",
                option_strings="--edition",
                nargs="*",
                help_string="Manually provide an 'edition' (e.g. Criterion Collection, Extended, Remastered, etc)",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-nfo",
                nargs=1,
                help_string="Use this to provide the path to an nfo file you want to upload",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-d",
                option_strings="--debug",
                action="store_true",
                help_string="Used for debugging. Writes debug lines to log file",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-dry",
                option_strings="--dry_run",
                action="store_true",
                help_string="Used for debugging. Writes debug lines to log and will also skip the upload",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-mkt",
                option_strings="--use_mktorrent",
                action="store_true",
                help_string="Use mktorrent instead of torf (Latest git version only)",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-fpm",
                option_strings="--force_pymediainfo",
                action="store_true",
                help_string="Force use PyMediaInfo to extract video codec over regex extraction from file name",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-r",
                option_strings="--resume",
                action="store_true",
                help_string="Resume previously unfinished upload.",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-3d",
                action="store_true",
                help_string="Mark the upload as 3D content",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-foreign",
                action="store_true",
                help_string="Mark the upload as foreign content [Non-English]",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-amf",
                option_strings="--allow_multiple_files",
                action="store_true",
                help_string="Override the default behavior and allow multiple files to be added in one torrent",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-ato",
                option_strings="--auto",
                action="store_true",
                help_string="Enabled auto mode for this particular upload",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-ss",
                option_strings="--skip_screenshots",
                action="store_true",
                help_string="Skip screenshot generation and upload for a run (overrides config.env)",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-disc",
                action="store_true",
                help_string="If you are uploading a raw dvd/bluray disc you need to pass this arg",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-let",
                option_strings="--load_external_templates",
                action="store_true",
                help_string="Load external site templates from ./external/site_templates location",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-tag",
                option_strings="--tags",
                nargs="*",
                help_string="Send custom tags to all trackers",
            ),
            GGBotArgumentType.UNCOMMON,
        )

        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-internal",
                action="store_true",
                help_string="(Internal) Used to mark an upload as 'Internal'",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-freeleech",
                action="store_true",
                help_string="(Internal) Used to give a new upload freeleech",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-personal",
                action="store_true",
                help_string="Mark an upload as personal release",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-featured",
                action="store_true",
                help_string="(Internal) feature a new upload",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-doubleup",
                action="store_true",
                help_string="(Internal) Give a new upload 'double up' status",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-tripleup",
                action="store_true",
                help_string="(Internal) Give a new upload 'triple up' status [XBTIT Exclusive]",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-sticky",
                action="store_true",
                help_string="(Internal) Pin the new upload",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-exclusive",
                nargs=1,
                choices=["0", "1", "2", "3"],
                help_string="(Internal) Set an upload as exclusive for n days",
            ),
            GGBotArgumentType.INTERNAL,
        )

        yield argument_config

    @pytest.fixture
    def argument_config_reuploader(self):
        argument_config = GGBotArgumentConfig(
            name="GG-BOT Auto Reuploader",
            description="An automated torrent re-uploading tool that monitors directories, updates metadata, and re-uploads to specified trackers with minimal user intervention.",
            epilog="Ensures torrents remain available by automating re-uploads. Configure settings properly before use. For more details, visit the official repository.",
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-t",
                option_strings="--trackers",
                nargs="*",
                help_string="Tracker(s) to upload to. Space-separates if multiple (no commas)",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-a",
                option_strings="--all_trackers",
                action="store_true",
                help_string="Select all trackers that can be uploaded to",
            ),
            GGBotArgumentType.COMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-anon",
                action="store_true",
                help_string="Tf you want your upload to be anonymous (no other info needed, just input '-anon'",
            ),
            GGBotArgumentType.COMMON,
        )

        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-d",
                option_strings="--debug",
                action="store_true",
                help_string="Used for debugging. Writes debug lines to log file",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-mkt",
                option_strings="--use_mktorrent",
                action="store_true",
                help_string="Use mktorrent instead of torf (Latest git version only)",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-fpm",
                option_strings="--force_pymediainfo",
                action="store_true",
                help_string="Force use PyMediaInfo to extract video codec over regex extraction from file name",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-ss",
                option_strings="--skip_screenshots",
                action="store_true",
                help_string="Skip screenshot generation and upload for a run (overrides config.env)",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-disc",
                action="store_true",
                help_string="Unsupported for AutoReuploader. Added for compatibility with upload assistant",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-let",
                option_strings="--load_external_templates",
                action="store_true",
                help_string="Load external site templates from ./external/site_templates location",
            ),
            GGBotArgumentType.UNCOMMON,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-tag",
                option_strings="--tags",
                nargs="*",
                help_string="Send custom tags to all trackers",
            ),
            GGBotArgumentType.UNCOMMON,
        )

        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-internal",
                action="store_true",
                help_string="(Internal) Used to mark an upload as 'Internal'",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-freeleech",
                action="store_true",
                help_string="(Internal) Used to give a new upload freeleech",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-featured",
                action="store_true",
                help_string="(Internal) feature a new upload",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-doubleup",
                action="store_true",
                help_string="(Internal) Give a new upload 'double up' status",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-tripleup",
                action="store_true",
                help_string="(Internal) Give a new upload 'triple up' status [XBTIT Exclusive]",
            ),
            GGBotArgumentType.INTERNAL,
        )
        argument_config.add_argument(
            GGBotArgumentEntry(
                dest="-sticky",
                action="store_true",
                help_string="(Internal) Pin the new upload",
            ),
            GGBotArgumentType.INTERNAL,
        )

        yield argument_config

    @pytest.mark.parametrize(
        "uploader_type",
        [
            pytest.param("UPLOAD_ASSISTANT", id="upload_assistant"),
            pytest.param("REUPLOADER", id="reuploader"),
        ],
    )
    def test_gg_bot_uploader_arg_parser(
        self,
        argument_config_reuploader,
        argument_config_upload_assistant,
        traditional_parser_upload_assistant,
        traditional_parser_reuploader,
        uploader_type,
    ):
        if uploader_type == "REUPLOADER":
            gg_bot_argument_config = argument_config_reuploader
            traditional_parser = traditional_parser_reuploader
        else:
            gg_bot_argument_config = argument_config_upload_assistant
            traditional_parser = traditional_parser_upload_assistant

        create_gg_bot_argument_parser_and_perform_assertions(
            gg_bot_argument_config, traditional_parser
        )
