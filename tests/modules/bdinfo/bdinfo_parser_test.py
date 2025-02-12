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
import shutil
from pathlib import Path

import pytest

from modules.bdinfo.bdinfo_parser import BDInfoParser
from modules.exceptions.exception import GGBotUploaderException

working_folder = Path(__file__).resolve().parent.parent.parent.parent

bdinfo_summary = "/tests/resources/bdinfo/summary/"
bdinfo_script_dummy = "/tests/resources/bdinfo/bdinfo_script_dummy"
bdinfo_upload_media = "/tests/resources/bdinfo/upload_media/"
bdinfo_metadata = "/tests/resources/bdinfo/metadata/"
bdinfo_metadata_expected = "/tests/resources/bdinfo/expected/"
bdinfo_working_folder = "/tests/resources/bdinfo/working_folder/"


def get_torrent_info(file_name):
    meta_data = json.load(open(f"{working_folder}{bdinfo_metadata}{file_name}.json"))

    torrent_info = {
        "upload_media": f"{working_folder}{bdinfo_working_folder}{file_name}/",
        "mediainfo": f"{working_folder}{bdinfo_working_folder}{file_name}/mediainfo.txt",
        "largest_playlist": meta_data["largest_playlist"],
        "raw_file_name": meta_data["raw_file_name"],
        "file_name": file_name,
        "raw_video_file": meta_data["raw_video_file"],
    }

    source = f"{working_folder}{bdinfo_summary}{file_name}.txt"
    destination = f'{working_folder}{bdinfo_working_folder}{file_name}/BDINFO.{torrent_info["raw_file_name"]}.txt'

    p = Path(f"{working_folder}{bdinfo_working_folder}{file_name}/")
    p.mkdir(parents=True, exist_ok=True)

    shutil.copy(source, destination)
    return torrent_info


def get_expected_bd_info(file_name):
    return json.load(
        open(f"{working_folder}{bdinfo_metadata_expected}{file_name}.json")
    )


def get_data_for_largest_playlist(file_name, override=None):
    data = json.load(open(f"{working_folder}{bdinfo_metadata}{file_name}.json"))
    return (
        f"{working_folder}{bdinfo_upload_media}{file_name}/",  # upload_media
        data["bdinfo_output_split"],  # sub_process_output
        data["largest_playlist"] if override is None else override,  # Expected
    )


# Mock side effects
def inside_container_side_effect(param, default=None):
    if param == "IS_CONTAINERIZED":
        return "True"
    return default


class TestBDInfoParser:
    @pytest.mark.parametrize(
        "upload_media",
        [
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED/",
                id="Company_Business",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME/",
                id="Dont_Breathe_2",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc/",
                id="Hardware",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}PIRATES_1_CURSE_OF_BLACK_PEARL/",
                id="Curse_of_black_perl",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Robot 2010 1080p Blu-ray AVC DTS-HD MA 5.1-DRs/",
                id="Robot",
            ),
        ],
    )
    def test_successful_parser_creation_in_container(self, mocker, upload_media):
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)
        parser = BDInfoParser(bdinfo_script="", upload_media=upload_media)
        assert parser is not None

    def test_parser_creation_without_bdmv_stream(self, mocker):
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)
        with pytest.raises(GGBotUploaderException) as ex:
            BDInfoParser(
                bdinfo_script="",
                upload_media=f"{working_folder}{bdinfo_upload_media}Pani.2024.COMPLETE.BLURAY-UNTOUCHED/",
            )
            assert (
                ex.message
                == "Currently unable to upload .iso files or disc/folders that does not contain a '/BDMV/STREAM/' "
                "folder"
            )

    @pytest.mark.parametrize(
        "upload_media",
        [
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED/",
                id="Company_Business",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME/",
                id="Dont_Breathe_2",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc/",
                id="Hardware",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}PIRATES_1_CURSE_OF_BLACK_PEARL/",
                id="Curse_of_black_perl",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Robot 2010 1080p Blu-ray AVC DTS-HD MA 5.1-DRs/",
                id="Robot",
            ),
        ],
    )
    def test_parser_creation_in_bare_metal(self, upload_media):
        parser = BDInfoParser(
            bdinfo_script=f"{working_folder}{bdinfo_script_dummy}",
            upload_media=upload_media,
        )
        assert parser is not None

    def test_parser_creation_in_bare_metal_without_bdinfo_script(self):
        with pytest.raises(GGBotUploaderException) as ex:
            BDInfoParser(
                bdinfo_script="placeholder",
                upload_media=f"{working_folder}{bdinfo_upload_media}Pani.2024.COMPLETE.BLURAY-UNTOUCHED/",
            )
            assert (
                ex.message
                == "The bdinfo script you specified: (placeholder) does not exist"
            )

    @pytest.mark.parametrize(
        ("upload_media", "sub_process_output", "expected"),
        [
            pytest.param(
                *get_data_for_largest_playlist(
                    "Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED"
                ),
                id="largest_playlist_1",
            ),
            pytest.param(
                *get_data_for_largest_playlist(
                    "Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME"
                ),
                id="largest_playlist_2",
            ),
            pytest.param(
                *get_data_for_largest_playlist(
                    "Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc"
                ),
                id="largest_playlist_3",
            ),
            pytest.param(
                *get_data_for_largest_playlist("PIRATES_1_CURSE_OF_BLACK_PEARL"),
                id="largest_playlist_4",
            ),
            pytest.param(
                *get_data_for_largest_playlist(
                    "Robot 2010 1080p Blu-ray AVC DTS-HD MA 5.1-DRs"
                ),
                id="largest_playlist_5",
            ),
        ],
    )
    def test_get_largest_playlist(
        self, mocker, upload_media, sub_process_output, expected
    ):
        mocker.patch("subprocess.check_output", return_value=sub_process_output)
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)

        parser = BDInfoParser(bdinfo_script="", upload_media=upload_media)
        assert parser.get_largest_playlist(True) == ("", expected)

    @pytest.mark.parametrize(
        ("upload_media", "sub_process_output", "expected", "user_choice"),
        [
            pytest.param(
                *get_data_for_largest_playlist(
                    "Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME",
                    "00380.MPLS",
                ),
                3,
                id="largest_playlist_manual_mode_2",
            ),
            pytest.param(
                *get_data_for_largest_playlist(
                    "Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc"
                ),
                1,
                id="largest_playlist_manual_mode_3",
            ),
            pytest.param(
                *get_data_for_largest_playlist(
                    "PIRATES_1_CURSE_OF_BLACK_PEARL", "01309.MPLS"
                ),
                3,
                id="largest_playlist_manual_mode_4",
            ),
            pytest.param(
                *get_data_for_largest_playlist(
                    "Robot 2010 1080p Blu-ray AVC DTS-HD MA 5.1-DRs"
                ),
                1,
                id="largest_playlist_manual_mode_5",
            ),
            pytest.param(
                *get_data_for_largest_playlist(
                    "Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED", "00004.MPLS"
                ),
                2,
                id="largest_playlist_manual_mode_override_user",
            ),
        ],
    )
    def test_get_largest_playlist_manual_mode(
        self, mocker, upload_media, sub_process_output, expected, user_choice
    ):
        mocker.patch("subprocess.check_output", return_value=sub_process_output)
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)
        mocker.patch("rich.prompt.Prompt.ask", return_value=user_choice)

        parser = BDInfoParser(bdinfo_script="", upload_media=upload_media)
        assert parser.get_largest_playlist(False) == ("", expected)

    @pytest.mark.parametrize(
        ("upload_media", "bdinfo", "expected"),
        [
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED/",
                get_expected_bd_info("Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED"),
                (None, "DTS-HD MA"),
                id="bdinfo_audio_codec_dtshdma",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME/",
                get_expected_bd_info(
                    "Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME"
                ),
                ("Atmos", "TrueHD"),
                id="bdinfo_audio_codec_truehd_atmos",
            ),
        ],
    )
    def test_get_audio_codec_from_bdinfo(self, mocker, upload_media, bdinfo, expected):
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)
        parser = BDInfoParser(bdinfo_script="", upload_media=upload_media)

        assert (
            parser.get_audio_codec_from_bdinfo(
                bdinfo,
                json.load(open(f"{working_folder}/parameters/audio_codecs.json")),
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("upload_media", "bdinfo", "expected"),
        [
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED/",
                get_expected_bd_info("Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED"),
                "2.0",
                id="bdinfo_audio_channels_2_0",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME/",
                get_expected_bd_info(
                    "Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME"
                ),
                "7.1",
                id="bdinfo_audio_channels_7_1",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc/",
                get_expected_bd_info(
                    "Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc"
                ),
                "5.1",
                id="bdinfo_audio_channels_5_1",
            ),
        ],
    )
    def test_get_audio_channels_from_bdinfo(
        self, mocker, upload_media, bdinfo, expected
    ):
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)
        parser = BDInfoParser(bdinfo_script="", upload_media=upload_media)

        assert parser.get_audio_channels_from_bdinfo(bdinfo) == expected

    @pytest.mark.parametrize(
        ("upload_media", "bdinfo", "expected"),
        [
            # TODO: Add tests for HDR10+ and DV
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED/",
                get_expected_bd_info("Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED"),
                (None, None, "AVC", "AVC"),
                id="bdinfo_video_codec_avc",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}PIRATES_1_CURSE_OF_BLACK_PEARL/",
                get_expected_bd_info("PIRATES_1_CURSE_OF_BLACK_PEARL"),
                (None, "HDR", "HEVC", "HEVC"),
                id="bdinfo_video_codec_",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME/",
                get_expected_bd_info(
                    "Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME"
                ),
                (None, "HDR", "HEVC", "HEVC"),
                id="bdinfo_video_codec_",
            ),
        ],
    )
    def test_get_video_codec_from_bdinfo(self, mocker, upload_media, bdinfo, expected):
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)
        parser = BDInfoParser(bdinfo_script="", upload_media=upload_media)

        assert parser.get_video_codec_from_bdinfo(bdinfo) == expected

    @pytest.mark.parametrize(
        ("upload_media", "torrent_info", "expected", "debug"),
        [
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED/",
                get_torrent_info("Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED"),
                get_expected_bd_info("Company.Business.1991.COMPLETE.BLURAY-UNTOUCHED"),
                False,  # debug
                id="bd_info_1",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME/",
                get_torrent_info(
                    "Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME"
                ),
                get_expected_bd_info(
                    "Dont.Breathe.2.2021.MULTi.COMPLETE.UHD.BLURAY-GLiMME"
                ),
                False,  # debug
                id="bd_info_2",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc/",
                get_torrent_info("Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc"),
                get_expected_bd_info(
                    "Hardware 1990 1080p Blu-ray AVC DD 5.1-BaggerInc"
                ),
                False,  # debug
                id="bd_info_3",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}PIRATES_1_CURSE_OF_BLACK_PEARL/",
                get_torrent_info("PIRATES_1_CURSE_OF_BLACK_PEARL"),
                get_expected_bd_info("PIRATES_1_CURSE_OF_BLACK_PEARL"),
                False,  # debug
                id="bd_info_4",
            ),
            pytest.param(
                f"{working_folder}{bdinfo_upload_media}Robot 2010 1080p Blu-ray AVC DTS-HD MA 5.1-DRs/",
                get_torrent_info("Robot 2010 1080p Blu-ray AVC DTS-HD MA 5.1-DRs"),
                get_expected_bd_info("Robot 2010 1080p Blu-ray AVC DTS-HD MA 5.1-DRs"),
                True,  # debug
                id="bd_info_5_debug",
            ),
        ],
    )
    def test_generate_and_parse_bdinfo(
        self, mocker, upload_media, torrent_info, expected, debug
    ):
        mocker.patch("os.getenv", side_effect=inside_container_side_effect)
        mocker.patch("subprocess.run", return_value=None)

        parser = BDInfoParser(bdinfo_script="", upload_media=upload_media)
        assert parser.generate_and_parse_bdinfo(torrent_info, debug) == expected
