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

from pathlib import Path
from unittest import mock

import pytest

from modules.description.description_manager import GGBotDescriptionManager


def clean_up(pth):
    pth = Path(pth)
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            clean_up(child)
    pth.rmdir()


class TestGGBotDescriptionManager:
    @pytest.fixture(scope="function")
    def setup_temp_upload_folder(self, working_folder_path):
        root_folder = f"{working_folder_path}/temp_upload"
        if Path(root_folder).is_dir():
            clean_up(root_folder)

        Path(f"{root_folder}/sub_folder").mkdir(parents=True, exist_ok=True)
        yield
        clean_up(root_folder)

    @pytest.mark.parametrize(
        ("tracker", "expected_template_name"),
        [
            pytest.param("blutopia", "blutopia.jinja2", id="default_template_exist"),
            pytest.param(
                "desitorrents", "desitorrents.jinja2", id="custom_template_exist"
            ),
            pytest.param(
                "passthepopcorn", "default.jinja2", id="fallback_to_default_template"
            ),
        ],
    )
    def test_manager_creation(
        self, working_folder_path, tracker, expected_template_name
    ):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker=tracker,
            source_type="",
            bbcode_line_break="\n",
        )
        assert manager is not None
        assert manager.template_manager is not None
        assert manager.template_manager.template is not None
        assert manager.template_manager.template.name == expected_template_name
        assert (
            manager._description_file_path
            == f"{working_folder_path}/temp_upload/sub_folder/{tracker}_description.txt"
        )

    def test_render(self, setup_temp_upload_folder, working_folder_path):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break="\n",
        )
        manager.description_file_data = {
            "custom_description_components": "CUSTOM_DESCRIPTION_COMPONENT",
            "internal": {
                "center_start": "[center]",
                "center_end": "[/center]",
                "uploader_signature": "SIGNATURE",
                "uploader_signature_hex": "SIGNATURE",
                "screenshot_header": "SCREENSHOT_HEADER",
            },
            "mediainfo": "",
            "screenshots": "SCREENSHOTS",
        }
        manager.render()

        with open(manager._description_file_path, "r") as description:
            rendered_description = description.read()
            assert (
                rendered_description
                == """CUSTOM_DESCRIPTION_COMPONENT

[center] SCREENSHOT_HEADER

SCREENSHOTS [/center]

[center] SIGNATURE [/center]"""
            )

    def test_set_custom_user_inputs_when_no_custom_inputs_available(
        self, working_folder_path
    ):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break="\n",
        )
        manager.set_custom_user_inputs(
            custom_user_inputs=None, tracker_description_components={}
        )

        assert (
            manager.description_file_data.get("custom_description_components")
            is not None
        )
        assert manager.description_file_data.get("custom_description_components") == ""
        assert (
            len(manager.description_file_data.get("custom_description_components")) == 0
        )

    def test_set_custom_user_inputs_tracker_do_not_support_description_components(
        self, working_folder_path
    ):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break="\n",
        )
        manager.set_custom_user_inputs(
            custom_user_inputs=[
                {
                    "key": "code_code",
                    "value": "This is a custom user component",
                    "title": "This is a title",
                }
            ],
            tracker_description_components=None,
        )

        assert (
            manager.description_file_data.get("custom_description_components")
            is not None
        )
        assert manager.description_file_data.get("custom_description_components") == ""
        assert (
            len(manager.description_file_data.get("custom_description_components")) == 0
        )

    @pytest.mark.parametrize(
        (
            "bbcode_line_break",
            "custom_user_inputs",
            "tracker_description_components",
            "expected_custom_description_components",
            "debug",
        ),
        [
            pytest.param(
                "\n",
                [
                    {
                        "key": "code_code",
                        "value": "This is a custom user component",
                        "title": "This is a title",
                    }
                ],
                {
                    "code_code": "[code][/code]",
                    "spoiler_code": "[spoiler=TITLE_PLACEHOLDER][/spoiler]",
                    "notes_code": "[note][/note]",
                    "quote_code": "[quote][/quote]",
                    "alert_code": "[alert][/alert]",
                },
                "[code]This is a custom user component[/code]\n",
                False,
                id="one_single_code_custom_description_with_\\n_line_break",
            ),
            pytest.param(
                "[br][/br]",
                [
                    {
                        "key": "code_code",
                        "value": "This is a custom user component",
                        "title": "This is a title",
                    }
                ],
                {
                    "code_code": "[code][/code]",
                    "spoiler_code": "[spoiler=TITLE_PLACEHOLDER][/spoiler]",
                    "notes_code": "[note][/note]",
                    "quote_code": "[quote][/quote]",
                    "alert_code": "[alert][/alert]",
                },
                "[code]This is a custom user component[/code][br][/br]",
                False,
                id="one_single_code_custom_description_with_[br][/br]_line_break",
            ),
            pytest.param(
                "<br />",
                [
                    {
                        "key": "code_code",
                        "value": "This is a custom user component",
                        "title": "This is a title",
                    }
                ],
                {
                    "code_code": "[code][/code]",
                    "spoiler_code": "[spoiler=TITLE_PLACEHOLDER][/spoiler]",
                    "notes_code": "[note][/note]",
                    "quote_code": "[quote][/quote]",
                    "alert_code": "[alert][/alert]",
                },
                "[code]This is a custom user component[/code]<br />",
                False,
                id="one_single_code_custom_description_with_<br />_line_break",
            ),
            pytest.param(
                "\n",
                [
                    {
                        "key": "code_code",
                        "value": "This is a custom user component",
                        "title": "This is a title",
                    },
                    {
                        "key": "code_code",
                        "value": "This is a another user component",
                        "title": "This is a title",
                    },
                    {
                        "key": "notes_code",
                        "value": "This is a notes custom user component",
                        "title": "",
                    },
                ],
                {
                    "code_code": "[code][/code]",
                    "spoiler_code": "[spoiler=TITLE_PLACEHOLDER][/spoiler]",
                    "quote_code": "[quote][/quote]",
                    "alert_code": "[alert][/alert]",
                },
                "[code]This is a custom user component[/code]\n[code]This is a another user component[/code]\nThis is a notes custom user component\n",
                False,
                id="multiple_code_custom_description",
            ),
            pytest.param(
                "\n",
                [
                    {
                        "key": "code_code",
                        "value": "this is one line code\n",
                        "title": "",
                    },
                    {
                        "key": "code_code",
                        "value": "this is second code without entering new linee that is multi line\n\nthis is the second line of second code block\n",
                        "title": "",
                    },
                    {
                        "key": "spoiler_code",
                        "value": "this is spoiler content multi line\nline 2\nline 3\n",
                        "title": "This is spoiler title",
                    },
                ],
                {
                    "code_code": "[code][/code]",
                    "spoiler_code": "<spoiler=TITLE_PLACEHOLDER></spoiler>",
                    "notes_code": "[note][/note]",
                    "quote_code": "[quote][/quote]",
                    "alert_code": "[alert][/alert]",
                },
                """[code]this is one line code
[/code]
[code]this is second code without entering new linee that is multi line

this is the second line of second code block
[/code]
<spoiler=This is spoiler title>this is spoiler content multi line
line 2
line 3
</spoiler>
""",
                True,
                id="multiple_code_and_spoiler_custom_description",
            ),
        ],
    )
    def test_set_custom_user_inputs(
        self,
        working_folder_path,
        custom_user_inputs,
        tracker_description_components,
        bbcode_line_break,
        debug,
        expected_custom_description_components,
    ):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break=bbcode_line_break,
            debug=debug,
        )
        manager.set_custom_user_inputs(
            custom_user_inputs=custom_user_inputs,
            tracker_description_components=tracker_description_components,
        )

        assert (
            manager.description_file_data["custom_description_components"]
            == expected_custom_description_components
        )

    def test_set_screenshots_without_any_screenshots(self, working_folder_path):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break="\n",
        )
        manager.set_screenshots(screenshots_data_types=None, screenshot_type=None)
        assert manager.description_file_data["screenshots"] == ""

    @pytest.mark.parametrize(
        ("screenshots_data_types", "screenshot_type", "expected_screenshots"),
        [
            pytest.param({}, None, "", id="screenshot_type_is_none"),
            pytest.param({}, "", "", id="screenshot_type_is_empty"),
            pytest.param(
                {
                    "type_1": "TYPE_1_DATA",
                    "type_2": "TYPE_2_DATA",
                },
                "type_1",
                "TYPE_1_DATA",
                id="screenshot_type_present_1",
            ),
            pytest.param(
                {
                    "type_1": "TYPE_1_DATA",
                    "type_2": "TYPE_2_DATA",
                },
                "type_2",
                "TYPE_2_DATA",
                id="screenshot_type_present_2",
            ),
        ],
    )
    def test_set_screenshots(
        self,
        working_folder_path,
        screenshots_data_types,
        screenshot_type,
        expected_screenshots,
    ):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break="\n",
        )
        manager.set_screenshots(
            screenshots_data_types=screenshots_data_types,
            screenshot_type=screenshot_type,
        )
        assert manager.description_file_data["screenshots"] == expected_screenshots

    def test_set_custom_uploader_signature_not_configured(self, working_folder_path):
        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break="\n",
        )
        default_signature = manager.description_file_data["internal"][
            "uploader_signature"
        ]
        manager.set_custom_uploader_signature()
        assert (
            manager.description_file_data["internal"]["uploader_signature"]
            == default_signature
        )

    @mock.patch("os.getenv")
    def test_set_custom_uploader_signature(self, mock_getenv, working_folder_path):
        custom_signature = "This is custom uploader signature"
        mock_getenv.return_value = custom_signature

        manager = GGBotDescriptionManager(
            working_folder=working_folder_path,
            sub_folder="sub_folder/",
            tracker="desitorrents",
            source_type="",
            bbcode_line_break="\n",
        )
        manager.set_custom_uploader_signature()
        assert (
            manager.description_file_data["internal"]["uploader_signature"]
            == f"[center]{custom_signature}[/center]\n[center]Powered by [url=https://gitlab.com/NoobMaster669/gg"
            f"-bot-upload-assistant]GG-BOT Upload Assistant[/url][/center]"
        )
