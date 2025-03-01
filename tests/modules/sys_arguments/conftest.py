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


import argparse

import pytest

from modules.sys_arguments.arg_config import GGBotArgumentConfig
from modules.sys_arguments.arg_parser import GGBotArgumentParser


@pytest.fixture(scope="module")
def traditional_parser_upload_assistant():
    # Setup args
    parser = argparse.ArgumentParser()

    # Required Arguments [Mandatory]
    required_args = parser.add_argument_group("Required Arguments")
    required_args.add_argument(
        "-p",
        "--path",
        nargs="*",
        required=True,
        help="Use this to provide path(s) to file/folder",
    )

    # Commonly used args:
    common_args = parser.add_argument_group("Commonly Used Arguments")
    common_args.add_argument(
        "-t",
        "--trackers",
        nargs="*",
        help="Tracker(s) to upload to. Space-separates if multiple (no commas)",
    )
    common_args.add_argument(
        "-a",
        "--all_trackers",
        action="store_true",
        help="Select all trackers that can be uploaded to",
    )
    common_args.add_argument(
        "-tmdb", nargs=1, help="Use this to manually provide the TMDB ID"
    )
    common_args.add_argument(
        "-imdb", nargs=1, help="Use this to manually provide the IMDB ID"
    )
    common_args.add_argument(
        "-tvmaze", nargs=1, help="Use this to manually provide the TVMaze ID"
    )
    common_args.add_argument(
        "-tvdb", nargs=1, help="Use this to manually provide the TVDB ID"
    )
    common_args.add_argument(
        "-mal",
        nargs=1,
        help="Use this to manually provide the MAL ID. If uploader detects any MAL id during search, this will be ignored.",
    )
    common_args.add_argument(
        "-anon",
        action="store_true",
        help="Tf you want your upload to be anonymous (no other info needed, just input '-anon'",
    )

    # Less commonly used args (Not essential for most)
    uncommon_args = parser.add_argument_group("Less Common Arguments")
    uncommon_args.add_argument(
        "-title", nargs=1, help="Custom title provided by the user"
    )
    uncommon_args.add_argument(
        "-rg",
        "--release_group",
        nargs=1,
        help="Set the release group for an upload",
    )
    uncommon_args.add_argument(
        "-type", nargs=1, help="Use to manually specify 'movie' or 'tv'"
    )
    uncommon_args.add_argument(
        "-reupload",
        nargs="*",
        help="This is used in conjunction with autodl to automatically re-upload any filter matches",
    )
    uncommon_args.add_argument(
        "-batch",
        action="store_true",
        help="Pass this arg if you want to upload all the files/folder within the folder you specify with the '-p' arg",
    )
    uncommon_args.add_argument(
        "-disc",
        action="store_true",
        help="If you are uploading a raw dvd/bluray disc you need to pass this arg",
    )
    uncommon_args.add_argument(
        "-e",
        "--edition",
        nargs="*",
        help="Manually provide an 'edition' (e.g. Criterion Collection, Extended, Remastered, etc)",
    )
    uncommon_args.add_argument(
        "-nfo",
        nargs=1,
        help="Use this to provide the path to an nfo file you want to upload",
    )
    uncommon_args.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Used for debugging. Writes debug lines to log file",
    )
    uncommon_args.add_argument(
        "-dry",
        "--dry_run",
        action="store_true",
        help="Used for debugging. Writes debug lines to log and will also skip the upload",
    )
    uncommon_args.add_argument(
        "-mkt",
        "--use_mktorrent",
        action="store_true",
        help="Use mktorrent instead of torf (Latest git version only)",
    )
    uncommon_args.add_argument(
        "-fpm",
        "--force_pymediainfo",
        action="store_true",
        help="Force use PyMediaInfo to extract video codec over regex extraction from file name",
    )
    uncommon_args.add_argument(
        "-ss",
        "--skip_screenshots",
        action="store_true",
        help="Skip screenshot generation and upload for a run (overrides config.env)",
    )
    uncommon_args.add_argument(
        "-r",
        "--resume",
        action="store_true",
        help="Resume previously unfinished upload.",
    )
    uncommon_args.add_argument(
        "-3d", action="store_true", help="Mark the upload as 3D content"
    )
    uncommon_args.add_argument(
        "-foreign",
        action="store_true",
        help="Mark the upload as foreign content [Non-English]",
    )
    uncommon_args.add_argument(
        "-amf",
        "--allow_multiple_files",
        action="store_true",
        help="Override the default behavior and allow multiple files to be added in one torrent",
    )
    uncommon_args.add_argument(
        "-let",
        "--load_external_templates",
        action="store_true",
        help="Load external site templates from ./external/site_templates location",
    )
    uncommon_args.add_argument(
        "-ato",
        "--auto",
        action="store_true",
        help="Enabled auto mode for this particular upload",
    )
    uncommon_args.add_argument(
        "-tag", "--tags", nargs="*", help="Send custom tags to all trackers"
    )

    # args for Internal uploads
    internal_args = parser.add_argument_group("Internal Upload Arguments")
    internal_args.add_argument(
        "-internal",
        action="store_true",
        help="(Internal) Used to mark an upload as 'Internal'",
    )
    internal_args.add_argument(
        "-freeleech",
        action="store_true",
        help="(Internal) Used to give a new upload freeleech",
    )
    internal_args.add_argument(
        "-featured", action="store_true", help="(Internal) feature a new upload"
    )
    internal_args.add_argument(
        "-personal", action="store_true", help="Mark an upload as personal release"
    )
    internal_args.add_argument(
        "-doubleup",
        action="store_true",
        help="(Internal) Give a new upload 'double up' status",
    )
    internal_args.add_argument(
        "-tripleup",
        action="store_true",
        help="(Internal) Give a new upload 'triple up' status [XBTIT Exclusive]",
    )
    internal_args.add_argument(
        "-sticky", action="store_true", help="(Internal) Pin the new upload"
    )
    internal_args.add_argument(
        "-exclusive",
        nargs=1,
        choices=["0", "1", "2", "3"],
        help="(Internal) Set an upload as exclusive for n days",
    )
    yield parser


@pytest.fixture(scope="module")
def traditional_parser_reuploader():
    # Setup args
    parser = argparse.ArgumentParser()

    common_args = parser.add_argument_group("Commonly Used Arguments")
    common_args.add_argument(
        "-t",
        "--trackers",
        nargs="*",
        help="Tracker(s) to upload to. Space-separates if multiple (no commas)",
    )
    common_args.add_argument(
        "-a",
        "--all_trackers",
        action="store_true",
        help="Select all trackers that can be uploaded to",
    )
    common_args.add_argument(
        "-anon",
        action="store_true",
        help="Tf you want your upload to be anonymous (no other info needed, just input '-anon'",
    )

    uncommon_args = parser.add_argument_group("Less Common Arguments")
    uncommon_args.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Used for debugging. Writes debug lines to log file",
    )
    uncommon_args.add_argument(
        "-mkt",
        "--use_mktorrent",
        action="store_true",
        help="Use mktorrent instead of torf (Latest git version only)",
    )
    uncommon_args.add_argument(
        "-fpm",
        "--force_pymediainfo",
        action="store_true",
        help="Force use PyMediaInfo to extract video codec over regex extraction from file name",
    )
    uncommon_args.add_argument(
        "-ss",
        "--skip_screenshots",
        action="store_true",
        help="Skip screenshot generation and upload for a run (overrides config.env)",
    )
    uncommon_args.add_argument(
        "-disc",
        action="store_true",
        help="Unsupported for AutoReuploader. Added for compatibility with upload assistant",
    )
    uncommon_args.add_argument(
        "-let",
        "--load_external_templates",
        action="store_true",
        help="Load external site templates from ./external/site_templates location",
    )
    uncommon_args.add_argument(
        "-tag", "--tags", nargs="*", help="Send custom tags to all trackers"
    )

    # args for Internal uploads
    internal_args = parser.add_argument_group("Internal Upload Arguments")
    internal_args.add_argument(
        "-internal",
        action="store_true",
        help="(Internal) Used to mark an upload as 'Internal'",
    )
    internal_args.add_argument(
        "-freeleech",
        action="store_true",
        help="(Internal) Used to give a new upload freeleech",
    )
    internal_args.add_argument(
        "-featured", action="store_true", help="(Internal) feature a new upload"
    )
    internal_args.add_argument(
        "-doubleup",
        action="store_true",
        help="(Internal) Give a new upload 'double up' status",
    )
    internal_args.add_argument(
        "-tripleup",
        action="store_true",
        help="(Internal) Give a new upload 'triple up' status [XBTIT Exclusive]",
    )
    internal_args.add_argument(
        "-sticky", action="store_true", help="(Internal) Pin the new upload"
    )
    yield parser


def create_gg_bot_argument_parser_and_perform_assertions(
    gg_bot_argument_config: GGBotArgumentConfig, traditional_parser
):
    parser = GGBotArgumentParser(gg_bot_argument_config)
    assert parser is not None

    arg_parser = parser._parser
    # Checking the values provided for argparse.ArgumentParser
    assert arg_parser.prog == gg_bot_argument_config.name
    assert arg_parser.description == gg_bot_argument_config.description
    assert arg_parser.epilog == gg_bot_argument_config.epilog

    # Verifying the actions / arguments supported
    assert len(arg_parser._actions) == len(traditional_parser._actions)

    # verify the count of each argument actions (StoreTrue, Store, Help etc)
    assert len(
        [
            action
            for action in arg_parser._actions
            if type(action) is argparse._StoreTrueAction
        ]
    ) == len(
        [
            action
            for action in traditional_parser._actions
            if type(action) is argparse._StoreTrueAction
        ]
    )

    assert len(
        [
            action
            for action in arg_parser._actions
            if type(action) is argparse._StoreAction
        ]
    ) == len(
        [
            action
            for action in traditional_parser._actions
            if type(action) is argparse._StoreAction
        ]
    )

    assert len(
        [
            action
            for action in arg_parser._actions
            if type(action) is argparse._HelpAction
        ]
    ) == len(
        [
            action
            for action in traditional_parser._actions
            if type(action) is argparse._HelpAction
        ]
    )

    # Now we compare the entire action list.
    # Here we first convert all actions to string and sort the list. This sorted string list is then compared
    sorted_expected_list = sorted(
        [str(action) for action in traditional_parser._actions]
    )
    sorted_actual_list = sorted([str(action) for action in arg_parser._actions])

    assert sorted_expected_list == sorted_actual_list
