from modules.description.template_manager import GGBotJinjaTemplateManager


class TestGGBotJinjaTemplateManager:
    def test_template_manager(self, working_folder_path):
        manager = GGBotJinjaTemplateManager(
            working_folder=working_folder_path, template_file_name="DT"
        )
        assert manager is not None
        assert manager.template is not None
        assert manager.template.name == "default.jinja2"

    def test_template_render(self, working_folder_path):
        manager = GGBotJinjaTemplateManager(
            working_folder=working_folder_path, template_file_name="DT"
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
