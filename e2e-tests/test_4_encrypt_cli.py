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

import shutil
import sys
from pathlib import Path
from unittest.mock import patch
from dotenv import load_dotenv
import pytest

from encrypt_cli import EncryptCLI
from modules.config import GGBotConfig
from utilities.utils import GenericUtils

parent_folder = Path(__file__).resolve().parent
test_config_for_encryption = "config-test-enc.env"
encrypted_file_name = "config.env"


class TestEncryptCLI:
    @pytest.fixture(scope="class")
    def working_folder(self):
        yield Path(parent_folder, "working_folder")

    @pytest.fixture(autouse=True)
    def run_around_tests(self, working_folder):
        working_folder.mkdir()
        shutil.copyfile(
            parent_folder / "resources" / test_config_for_encryption,
            working_folder / test_config_for_encryption,
        )
        yield
        shutil.rmtree(working_folder)

    def test_key_generation(self, working_folder):
        test_args = [
            "encrypt_cli.py",
            "generate-keys",
            "--private-key",
            str(working_folder / "private_key.pem"),
            "--public-key",
            str(working_folder / "public_key.pem"),
        ]

        with patch.object(sys, "argv", test_args):
            cli = EncryptCLI()
            cli.run()

        assert Path(working_folder / "private_key.pem").exists()
        assert Path(working_folder / "public_key.pem").exists()

    def test_encrypt_cli(self, working_folder):
        # First we are going to generate keys
        self.test_key_generation(working_folder=working_folder)
        test_args = [
            "encrypt_cli.py",
            "encrypt",
            "-i",
            str(working_folder / test_config_for_encryption),
            "-o",
            str(working_folder / encrypted_file_name),
            "-k",
            str(working_folder / "public_key.pem"),
            "--private-key",
            str(working_folder / "private_key.pem"),
        ]

        with patch.object(sys, "argv", test_args):
            cli = EncryptCLI()
            cli.run()

        assert Path(working_folder / test_config_for_encryption).exists()
        assert Path(working_folder / encrypted_file_name).exists()

        with open(working_folder / encrypted_file_name, "rb") as encrypted_file:
            encrypted_data = str(encrypted_file.read())
            assert str(working_folder / "private_key.pem") in encrypted_data

        load_dotenv(working_folder / encrypted_file_name, override=True)

        GenericUtils.initialize_decryptor()
        assert GGBotConfig().get_config("ACM_API_KEY") == "PLACEHOLDER_API_KEY"
        assert GGBotConfig().get_config("BHD_API_KEY") == "PLACEHOLDER_API_KEY"
        assert GGBotConfig().get_config("PTP_API_USER") == "PLACEHOLDER_API_KEY"
        assert GGBotConfig().get_config("PTP_API_KEY") == "PLACEHOLDER_API_KEY"
        assert GGBotConfig().get_config("PTP_2FA_CODE") == "PLACEHOLDER_API_KEY"
        assert (
            GGBotConfig().get_config("PTP_USER_PASSWORD")
            == "13asdiasdsd7W^tBs12342wqsdre32wx39##q247N!Tax!W"
        )
        assert GGBotConfig().get_config("TMDB_API_KEY") == "PLACEHOLDER_API_KEY"
        assert GGBotConfig().get_config("IMDB_API_KEY") == "PLACEHOLDER_API_KEY"
