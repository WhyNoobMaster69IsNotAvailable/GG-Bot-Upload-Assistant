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

import os
import sys
from pathlib import Path
from unittest import mock

from auto_upload import GGBotUploadAssistant
from modules.cryptography.key_manager import KeyManager
from modules.cryptography.encrypt_decrypt_processor import EncryptProcessor


class TestGGBotUploadAssistantWithEncryption:
    """Tests for GGBotUploadAssistant with encrypted configuration."""

    @classmethod
    def setup_class(cls):
        """Set up encryption keys and encrypted config for the test class."""
        cls.working_folder = Path(__file__).resolve().parent
        cls.private_key_path = f"{cls.working_folder}/resources/test_private_key.pem"
        cls.public_key_path = f"{cls.working_folder}/resources/test_public_key.pem"

        # Generate keys if they don't exist
        if (
            not Path(cls.private_key_path).exists()
            or not Path(cls.public_key_path).exists()
        ):
            key_manager = KeyManager(
                private_key_path=cls.private_key_path,
                public_key_path=cls.public_key_path,
            )
            key_manager.generate_and_save_keys(force_overwrite=True)

        # Create encrypted config file
        cls.create_encrypted_config()

    @classmethod
    def create_encrypted_config(cls):
        """Create an encrypted config file for testing."""
        # Read the test config
        with open(f"{cls.working_folder}/resources/config-test.env", "r") as f:
            config_content = f.read()

        # Add some sensitive values to encrypt
        config_lines = config_content.split("\n")
        modified_config_lines = []

        for line in config_lines:
            if line.startswith("TMDb_API_KEY="):
                modified_config_lines.append(line + " # ENCRYPT")
            elif line.startswith("TSP_API_KEY="):
                modified_config_lines.append(line + " # ENCRYPT")
            else:
                modified_config_lines.append(line)

        modified_config = "\n".join(modified_config_lines)

        # Create source config file to encrypt
        with open(
            f"{cls.working_folder}/resources/config-test-to-encrypt.env", "w"
        ) as f:
            f.write(modified_config)

        # Load public key and encrypt
        key_manager = KeyManager(public_key_path=cls.public_key_path)
        public_key = key_manager.load_public_key()
        encryptor = EncryptProcessor(public_key)

        from modules.cryptography.env_processor import EnvFileProcessor

        processor = EnvFileProcessor(encryptor)
        processor.process_file(
            f"{cls.working_folder}/resources/config-test-to-encrypt.env",
            f"{cls.working_folder}/resources/config-test-encrypted.env",
        )

    @mock.patch.object(
        sys,
        "argv",
        [
            "test.py",
            "-t",
            "TSP",
            "-p",
            "./resources/Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv",
            "--auto",
            "--debug",
        ],
    )
    def test_upload_assistant_with_encrypted_config(self, e2e_test_working_folder):
        """Test upload assistant with encrypted configuration file."""
        # Temporarily set PRIVATE_KEY_PATH environment variable
        old_env = os.environ.get("PRIVATE_KEY_PATH")
        os.environ["PRIVATE_KEY_PATH"] = self.private_key_path

        try:
            # Create and run upload assistant with encrypted config
            assistant = GGBotUploadAssistant(
                f"{self.working_folder}/resources/config-test-encrypted.env"
            )
            assistant.start(
                [
                    f"{e2e_test_working_folder}/e2e-tests/resources/Deadpool.&.Wolverine.2024.2160p.AMZN.WEB-DL.HDR.DDP.5.1.H.264-ReleaseGroup.mkv"
                ]
            )

            # Verify that initialization and decryption worked
            assert assistant.api_keys_dict != {}
            assert "tmdb_api_key" in assistant.api_keys_dict
            assert "TSP_api_key" in assistant.api_keys_dict

            # Verify media info was parsed successfully
            assert assistant.torrent_info != {}
            assert assistant.torrent_info["title"] == "Deadpool & Wolverine"
            assert assistant.torrent_info["year"] == "2024"
            assert assistant.torrent_info["screen_size"] == "2160p"
            assert assistant.torrent_info["video_codec"] == "H.264"

            # Verify upload was successful
            assert assistant.torrent_info["TSP_upload_status"] is True
        finally:
            # Restore environment
            if old_env is not None:
                os.environ["PRIVATE_KEY_PATH"] = old_env
            else:
                del os.environ["PRIVATE_KEY_PATH"]
