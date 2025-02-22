from pathlib import Path

import pytest

from modules.sys_arguments.arg_reader import GGBotArgReader
from tests.modules.sys_arguments.conftest import (
    create_gg_bot_argument_parser_and_perform_assertions,
)

working_folder = Path(__file__).resolve().parent.parent.parent.parent


class TestGGBotArgReader:
    @pytest.mark.parametrize(
        ("config_file", "traditional_args"),
        [
            pytest.param(
                f"{working_folder}/parameters/sys_args/upload_assistant.yml",
                "UPLOAD_ASSISTANT",
                id="upload_assistant",
            ),
            pytest.param(
                f"{working_folder}/parameters/sys_args/reuploader.yml",
                "REUPLOADER",
                id="reuploader",
            ),
        ],
    )
    def test_gg_bot_uploader_config(
        self,
        config_file,
        traditional_args,
        traditional_parser_upload_assistant,
        traditional_parser_reuploader,
    ):
        # I know this is not a good approach. By too lazy to use metafunc
        if traditional_args == "REUPLOADER":
            traditional_parser = traditional_parser_reuploader
        else:
            traditional_parser = traditional_parser_upload_assistant

        arg_reader = GGBotArgReader(config_file)
        uploader_config = arg_reader.read_and_get_config()

        create_gg_bot_argument_parser_and_perform_assertions(
            uploader_config, traditional_parser
        )
