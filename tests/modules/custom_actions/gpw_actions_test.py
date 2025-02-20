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
import pytest
import shutil

from pathlib import Path

import modules.custom_actions.gpw_actions as gpw_actions


working_folder = Path(__file__).resolve().parent.parent.parent.parent
temp_working_dir = "/tests/working_folder/gpw_rehost/"


@pytest.fixture(scope="function")
def prepare_working_folder():
    folder = f"{working_folder}{temp_working_dir}"

    if Path(folder).is_dir():
        clean_up(folder)

    shutil.copytree(
        f"{working_folder}/tests/resources/custom_actions/gpw/rehost_data",
        f"{working_folder}{temp_working_dir}",
    )
    yield
    clean_up(folder)


def clean_up(pth):
    pth = Path(pth)
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            clean_up(child)
    pth.rmdir()


class APIResponse:
    ok = None
    data = None
    url = None

    def __init__(self, data, text=None, url=None):
        self.ok = "True"
        self.data = data
        self.text = text
        self.url = url

    def json(self):
        return self.data


def test_check_for_existing_group_no_group(monkeypatch, mocker):
    torrent_info = {
        "imdb_with_tt": "tt10954600",
        "title": "AntMan and the Wasp Quantumania",
        "tmdb_metadata": {
            "tags": [],
            "poster": "https://www.themoviedb.org/t/p/w600_and_h900_bestv2/fa9TNxYyDdRcFAPJ6rvKf3ZrVtB.jpg",
        },
        "imdb_metadata": {"tags": [], "poster": ""},
        "year": "2022",
    }
    tracker_config = dict()
    tracker_config["upload_form"] = "http://gpw.com/{api_key}&action=upload"
    tracker_settings = {}

    check_group_response = APIResponse(
        json.load(
            open(
                f"{working_folder}/tests/resources/custom_action_responses/gpw_no_group.json"
            )
        )
    )
    autofill_response = APIResponse(
        json.load(
            open(
                f"{working_folder}/tests/resources/custom_action_responses/gpw_auto_fill.json"
            )
        )
    )
    gpw_responses = iter([check_group_response, autofill_response])
    monkeypatch.setattr("requests.get", lambda url: next(gpw_responses))
    mocker.patch("os.getenv", return_value="GPW_API_KEY")

    gpw_actions.check_for_existing_group(torrent_info, tracker_settings, tracker_config)

    assert tracker_settings["releasetype"] == "1"
    assert tracker_settings["name"] == "Ant-Man and the Wasp: Quantumania"
    assert tracker_settings["image"] == torrent_info["tmdb_metadata"]["poster"]
    assert tracker_settings["year"] == "2023"
    assert tracker_settings["tags"] == "action,adventure,comedy"
    assert (
        tracker_settings["maindesc"]
        == "Scott Lang and Hope Van Dyne, along with Hank Pym and Janet Van Dyne, explore the Quantum Realm, where they interact with strange creatures and embark on an adventure that goes beyond the limits of what they thought was possible."
    )
    assert tracker_settings["desc"] == tracker_settings["maindesc"]
    assert tracker_settings["artist_ids[]"] == [
        "nm0715636",
        "nm0456158",
        "nm3278218",
        "nm0068416",
        "nm0112780",
        "nm0209326",
        "nm0270559",
        "nm0065100",
        "nm0748620",
        "nm1431940",
        "nm3718007",
        "nm1105980",
        "nm0000201",
        "nm0000195",
        "nm0000140",
        "nm1320827",
        "nm1015684",
        "nm10054154",
        "nm11395022",
        "nm3432428",
        "nm13148405",
        "nm11105476",
    ]
    assert tracker_settings["artists[]"] == [
        "Peyton Reed",
        "Jack Kirby",
        "Jeff Loveness",
        "Mitchell Bell",
        "Stephen Broussard",
        "Kevin de la Noy",
        "Kevin Feige",
        "Christophe Beck",
        "Paul Rudd",
        "Evangeline Lilly",
        "Jonathan Majors",
        "Kathryn Newton",
        "Michelle Pfeiffer",
        "Bill Murray",
        "Michael Douglas",
        "Randall Park",
        "Corey Stoll",
        "Leonardo Taiwo",
        "Mike Wood",
        "David Bertucci",
        "Paul Fairlie",
        "Tony McCarthy",
    ]
    assert tracker_settings["importance[]"] == [
        1,
        2,
        2,
        3,
        3,
        3,
        3,
        4,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
    ]
    assert tracker_settings["artists_sub[]"] == [
        "" for x in range(0, len(tracker_settings["importance[]"]))
    ]
    assert "groupid" not in tracker_settings


def test_check_for_existing_group_group_exists(monkeypatch, mocker):
    torrent_info = {"imdb_with_tt": "tt1630029"}
    tracker_config = dict()
    tracker_config["upload_form"] = "http://gpw.com/{api_key}&action=upload"
    tracker_settings = {}

    mocker.patch(
        "requests.get",
        return_value=APIResponse(
            json.load(
                open(
                    f"{working_folder}/tests/resources/custom_action_responses/gpw_group_exist.json"
                )
            )
        ),
    )

    gpw_actions.check_for_existing_group(torrent_info, tracker_settings, tracker_config)
    assert tracker_settings["groupid"] == 54321


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        pytest.param(
            APIResponse(
                json.load(
                    open(
                        f"{working_folder}/tests/resources/custom_action_responses/gpw_upload_successful.json"
                    )
                )
            ),
            (True, "Successfully uploaded torrent to GPW"),
            id="upload_successful",
        ),
        pytest.param(
            APIResponse(
                json.load(
                    open(
                        f"{working_folder}/tests/resources/custom_action_responses/gpw_upload_failed.json"
                    )
                )
            ),
            (False, "Usually a meaningful error"),
            id="upload_failed",
        ),
    ],
)
def test_check_successful_upload(response, expected):
    assert gpw_actions.check_successful_upload(response) == expected


@pytest.mark.parametrize(
    ("subtitles", "expected_type", "expected_values"),
    [
        pytest.param(
            [
                {"language_code": "es"},
                {"language_code": "far"},
                {"language_code": "", "title": "Icelandic"},
                {"language_code": "", "title": "Invalid_sub"},
            ],
            1,  # softcoded
            ["spanish", "persian", "icelandic"],
            id="soft_coded_subs",
        ),
        pytest.param(
            [
                {"language_code": "", "title": "Invalid_sub"},
            ],
            3,  # no_subs
            [],
            id="no_subs",
        ),
        pytest.param([], 3, [], id="no_subs"),  # no_subs
    ],
)
def test_add_subtitle_information(subtitles, expected_type, expected_values):
    torrent_info = {"subtitles": subtitles}
    tracker_settings = {}
    gpw_actions.add_subtitle_information(torrent_info, tracker_settings, {})
    assert tracker_settings["subtitle_type"] == expected_type
    assert tracker_settings["subtitles[]"] == expected_values


def __get_torrent_info_for_rehost_test(test_id):
    return {
        **json.load(
            open(
                f"{working_folder}/tests/resources/custom_actions/gpw/rehost_data/{test_id}/torrent_info.json"
            )
        ),
        "screenshots_data": f"{working_folder}{temp_working_dir}{test_id}/screenshots_data.json",
    }


def __get_expected_for_rehost_test(test_id):
    return {
        **json.load(
            open(
                f"{working_folder}/tests/resources/custom_actions/gpw/rehost_data/{test_id}/expected.json"
            )
        ),
        "mock_return": f"{working_folder}{temp_working_dir}{test_id}/mock_upload_response.json",
    }


@pytest.mark.parametrize(
    ("torrent_info", "expected"),
    [
        pytest.param(
            __get_torrent_info_for_rehost_test(test_id=1),
            __get_expected_for_rehost_test(test_id=1),
            id="nothing_to_rehost",
        ),
        pytest.param(
            __get_torrent_info_for_rehost_test(test_id=2),
            __get_expected_for_rehost_test(test_id=2),
            id="already_rehosted",
        ),
        pytest.param(
            __get_torrent_info_for_rehost_test(test_id=3),
            __get_expected_for_rehost_test(test_id=3),
            id="something_to_rehost",
        ),
    ],
)
def test_rehost_screens(torrent_info, expected, mocker, prepare_working_folder):
    tracker_settings = dict()
    mocker.patch(
        "requests.post",
        return_value=APIResponse(json.load(open(expected["mock_return"]))),
    )

    gpw_actions.rehost_screens(
        torrent_info,
        tracker_settings,
        {"upload_form": "https://url.com/upload.php?api_key={api_key}&action=upload"},
    )

    assert tracker_settings["gpw_rehosted"] == expected["gpw_rehosted"]
    screenshots_data = json.load(open(torrent_info["screenshots_data"]))
    assert screenshots_data == expected["screenshots_data"]


def test_rehost_screens_with_no_screenshots(prepare_working_folder):
    assert (
        gpw_actions.rehost_screens(
            {},
            {},
            {
                "upload_form": "https://url.com/upload.php?api_key={api_key}&action=upload"
            },
        )
        is None
    )


def test_rehost_screens_with_exception_from_tracker(mocker, prepare_working_folder):
    torrent_info = {
        **json.load(
            open(
                f"{working_folder}/tests/resources/custom_actions/gpw/rehost_data/4/torrent_info.json"
            )
        ),
        "screenshots_data": f"{working_folder}{temp_working_dir}4/screenshots_data.json",
    }
    expected = {
        **json.load(
            open(
                f"{working_folder}/tests/resources/custom_actions/gpw/rehost_data/4/expected.json"
            )
        ),
        "mock_return": f"{working_folder}{temp_working_dir}4/mock_upload_response.json",
    }
    mocker.patch(
        "requests.post",
        return_value=APIResponse(json.load(open(expected["mock_return"]))),
    )

    with pytest.raises(Exception):
        gpw_actions.rehost_screens(
            torrent_info,
            {},
            {
                "upload_form": "https://url.com/upload.php?api_key={api_key}&action=upload"
            },
        )
