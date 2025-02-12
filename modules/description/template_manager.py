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
from typing import Dict

from jinja2 import FileSystemLoader, Environment

from modules.constants import DESCRIPTIONS_TEMPLATE_PATH, DEFAULT_DESCRIPTION_TEMPLATE


class GGBotJinjaTemplateManager:
    def __init__(self, *, working_folder: str, template_file_name: str):
        self.template_file_name = template_file_name
        self.working_folder = working_folder
        self.template = self._load_jinja_template()

    def _load_jinja_template(self):
        templates_folder = self._get_templates_folder()
        template_file = self._get_template_file(templates_folder)

        template_loader = FileSystemLoader(searchpath=templates_folder)
        template_environment = Environment(loader=template_loader, autoescape=True)

        return template_environment.get_template(template_file)

    def _get_template_file(self, templates_folder):
        if Path(f"{templates_folder}/{self.template_file_name}.jinja2").exists():
            return f"{self.template_file_name}.jinja2"

        return DEFAULT_DESCRIPTION_TEMPLATE

    def _get_templates_folder(self):
        return DESCRIPTIONS_TEMPLATE_PATH.format(base_path=self.working_folder)

    def render(self, data: Dict):
        return self.template.render(data=data)
