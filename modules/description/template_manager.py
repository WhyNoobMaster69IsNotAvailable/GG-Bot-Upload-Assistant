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
from typing import Dict, List

from jinja2 import FileSystemLoader, Environment

from modules.constants import (
    DESCRIPTIONS_TEMPLATE_PATH,
    DEFAULT_DESCRIPTION_TEMPLATE,
    DESCRIPTIONS_CUSTOM_TEMPLATE_PATH,
)


class GGBotJinjaTemplateManager:
    def __init__(self, *, working_folder: str, template_name: str, source_type: str):
        self.template_name = template_name
        self.source_type = source_type
        self.working_folder = working_folder
        self.template = self._load_jinja_template()

    def _load_jinja_template(self):
        templates_folders: List[str] = self._get_templates_folders()
        template_file = self._get_template_file(templates_folders)

        template_loader = FileSystemLoader(searchpath=templates_folders)
        template_environment = Environment(loader=template_loader, autoescape=True)

        return template_environment.get_template(template_file)

    def _get_template_file(self, templates_folders: List[str]):
        # here we first look for source type specific template in both custom and default folder
        # if source type based is not found, then we look for tracker specific template
        # in case if tracker specific template is missing, we fall back to default template
        for folder in templates_folders:
            if not Path(
                f"{folder}/{self.template_name}-{self.source_type}.jinja2"
            ).exists():
                continue
            return f"{self.template_name}-{self.source_type}.jinja2"

        for folder in templates_folders:
            if not Path(f"{folder}/{self.template_name}.jinja2").exists():
                continue
            return f"{self.template_name}.jinja2"

        return DEFAULT_DESCRIPTION_TEMPLATE

    def _get_templates_folders(self) -> List[str]:
        # The order matters here. We first check custom templates folder and then fallback to default templates
        return [
            DESCRIPTIONS_CUSTOM_TEMPLATE_PATH.format(base_path=self.working_folder),
            DESCRIPTIONS_TEMPLATE_PATH.format(base_path=self.working_folder),
        ]

    def render(self, data: Dict):
        return self.template.render(data=data)
