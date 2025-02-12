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
        template_environment = Environment(loader=template_loader)

        return template_environment.get_template(template_file)

    def _get_template_file(self, templates_folder):
        if Path(f"{templates_folder}/{self.template_file_name}.jinja2").exists():
            return f"{self.template_file_name}.jinja2"

        return DEFAULT_DESCRIPTION_TEMPLATE

    def _get_templates_folder(self):
        return DESCRIPTIONS_TEMPLATE_PATH.format(base_path=self.working_folder)

    def render(self, data: Dict):
        return self.template.render(data=data)
