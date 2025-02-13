# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669
import pytest

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

from modules.description.template_manager import GGBotJinjaTemplateManager


class TestGGBotJinjaTemplateManager:
    @pytest.mark.parametrize(
        ("template_name", "source_type", "loaded_template_name"),
        [
            pytest.param("passthepopcorn", "", "default.jinja2", id="default_template"),
            pytest.param("blutopia", "", "blutopia.jinja2", id="built_in_template"),
            pytest.param(
                "blutopia",
                "webdl",
                "blutopia-webdl.jinja2",
                id="built_in_template_with_source",
            ),
            pytest.param(
                "blutopia",
                "remux",
                "blutopia-remux.jinja2",
                id="built_in_template_with_source_2",
            ),
            pytest.param(
                "blutopia",
                "encode",
                "blutopia.jinja2",
                id="built_in_template_with_missing_source",
            ),
            pytest.param(
                "desitorrents", "", "desitorrents.jinja2", id="custom_template"
            ),
            pytest.param(
                "desitorrents",
                "webdl",
                "desitorrents-webdl.jinja2",
                id="custom_template_with_source",
            ),
            pytest.param(
                "desitorrents",
                "encode",
                "desitorrents.jinja2",
                id="custom_template_with_missing_source",
            ),
        ],
    )
    def test_template_manager(
        self, working_folder_path, template_name, loaded_template_name, source_type
    ):
        manager = GGBotJinjaTemplateManager(
            working_folder=working_folder_path,
            template_name=template_name,
            source_type=source_type,
        )
        assert manager is not None
        assert manager.template is not None
        assert manager.template.name == loaded_template_name

    def test_template_render(self, working_folder_path):
        manager = GGBotJinjaTemplateManager(
            working_folder=working_folder_path, template_name="DT", source_type=""
        )

        data = {
            "custom_description_components": "CUSTOM_DESCRIPTION_COMPONENT",
            "internal": {
                "center_start": "[center]",
                "center_end": "[/center]",
                "uploader_signature": "SIGNATURE",
                "screenshot_header": "SCREENSHOT_HEADER",
            },
            "screenshots": "SCREENSHOTS",
        }
        result = manager.render(data=data)
        assert (
            result
            == """CUSTOM_DESCRIPTION_COMPONENT

[center] SCREENSHOT_HEADER

SCREENSHOTS [/center]

[center] SIGNATURE [/center]"""
        )
