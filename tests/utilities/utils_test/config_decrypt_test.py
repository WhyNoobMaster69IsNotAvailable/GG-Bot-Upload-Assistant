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

import pytest
import os
from unittest.mock import MagicMock

# Assuming these modules/classes exist based on the function's code
import modules.config
from utilities.utils import GenericUtils
from modules.exceptions.exception import GGBotFatalException
from modules.cryptography.key_manager import KeyManager
from modules.cryptography.encrypt_decrypt_processor import DecryptProcessor


# --- Tests for initialize_decryptor --- #
class TestConfigDecrypt:
    def test_initialize_decryptor_success(self, mocker, caplog):
        """Test successful initialization when PRIVATE_KEY_PATH is set and valid."""
        # Arrange
        mock_key_manager_instance = MagicMock(spec=KeyManager)
        mock_private_key = MagicMock()
        mock_key_manager_instance.load_private_key.return_value = mock_private_key
        mock_decryptor_instance = MagicMock(spec=DecryptProcessor)

        mocker.patch("os.getenv", return_value="/fake/path/key.pem")
        # Patch the classes within the module where they are used
        mock_keymanager_class = mocker.patch(
            "utilities.utils.KeyManager", return_value=mock_key_manager_instance
        )
        mock_decryptor_class = mocker.patch(
            "utilities.utils.DecryptProcessor", return_value=mock_decryptor_instance
        )
        mocker.patch("modules.config.global_decryptor_instance", None, create=True)

        # Act
        GenericUtils.initialize_decryptor()

        # Assert
        assert modules.config.global_decryptor_instance == mock_decryptor_instance
        assert os.getenv.call_count == 1
        assert os.getenv.call_args[0][0] == "PRIVATE_KEY_PATH"
        # Assert call_count on the mock class object
        assert mock_keymanager_class.call_count == 1
        assert (
            mock_keymanager_class.call_args[1]["private_key_path"]
            == "/fake/path/key.pem"
        )
        mock_key_manager_instance.load_private_key.assert_called_once()
        # Assert call on the mock class object
        mock_decryptor_class.assert_called_once_with(mock_private_key)
        assert (
            "Private key loaded successfully. Config decryption enabled." in caplog.text
        )

    def test_initialize_decryptor_no_path(self, mocker, caplog):
        """Test initialization when PRIVATE_KEY_PATH is not set."""
        # Arrange
        mocker.patch("os.getenv", return_value=None)
        mocker.patch("modules.config.global_decryptor_instance", None, create=True)
        # Patch the classes within the module where they are used
        mock_keymanager_class = mocker.patch("utilities.utils.KeyManager")
        mock_decryptor_class = mocker.patch("utilities.utils.DecryptProcessor")

        # Act
        GenericUtils.initialize_decryptor()

        # Assert
        assert modules.config.global_decryptor_instance is None
        assert os.getenv.call_count == 1
        assert os.getenv.call_args[0][0] == "PRIVATE_KEY_PATH"
        # Assert call_count on the mock class objects
        assert mock_keymanager_class.call_count == 0
        assert mock_decryptor_class.call_count == 0
        assert (
            "PRIVATE_KEY_PATH not set. Configuration decryption disabled."
            in caplog.text
        )

    def test_initialize_decryptor_fatal_exception(self, mocker, caplog):
        """Test initialization failure due to GGBotFatalException during key loading."""
        # Arrange
        mock_key_manager_instance = MagicMock(spec=KeyManager)
        load_error = GGBotFatalException("Bad key file")
        mock_key_manager_instance.load_private_key.side_effect = load_error

        mocker.patch("os.getenv", return_value="/fake/path/bad_key.pem")
        # Patch the classes within the module where they are used
        mock_keymanager_class = mocker.patch(
            "utilities.utils.KeyManager", return_value=mock_key_manager_instance
        )
        mock_decryptor_class = mocker.patch("utilities.utils.DecryptProcessor")
        mocker.patch("modules.config.global_decryptor_instance", None, create=True)

        # Act & Assert
        with pytest.raises(GGBotFatalException) as excinfo:
            GenericUtils.initialize_decryptor()

        assert excinfo.value == load_error
        assert modules.config.global_decryptor_instance is None
        # Assert call_count on the mock class objects
        assert mock_keymanager_class.call_count == 1
        mock_key_manager_instance.load_private_key.assert_called_once()
        assert mock_decryptor_class.call_count == 0
        assert "FAILED TO LOAD PRIVATE KEY" in caplog.text
        assert "Encrypted configuration values will NOT be decrypted." in caplog.text

    def test_initialize_decryptor_generic_exception(self, mocker, caplog):
        """Test initialization failure due to a generic Exception during key loading."""
        # Arrange
        mock_key_manager_instance = MagicMock(spec=KeyManager)
        load_error = ValueError("Unexpected format")
        mock_key_manager_instance.load_private_key.side_effect = load_error

        mocker.patch("os.getenv", return_value="/fake/path/weird_key.pem")
        # Patch the classes within the module where they are used
        mock_keymanager_class = mocker.patch(
            "utilities.utils.KeyManager", return_value=mock_key_manager_instance
        )
        mock_decryptor_class = mocker.patch("utilities.utils.DecryptProcessor")
        mocker.patch("modules.config.global_decryptor_instance", None, create=True)

        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            GenericUtils.initialize_decryptor()

        assert excinfo.value == load_error
        assert modules.config.global_decryptor_instance is None
        # Assert call_count on the mock class objects
        assert mock_keymanager_class.call_count == 1
        mock_key_manager_instance.load_private_key.assert_called_once()
        assert mock_decryptor_class.call_count == 0
        assert "UNEXPECTED ERROR loading private key" in caplog.text
        assert "Encrypted configuration values will NOT be decrypted." in caplog.text
