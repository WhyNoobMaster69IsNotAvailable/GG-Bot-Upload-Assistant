# GG Bot Upload Assistant
# Copyright (C) 2022  Noob Master669

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
from unittest.mock import patch, MagicMock, mock_open
import sys
import argparse
from pathlib import Path

# We need to be able to import the script to test its classes/functions
# Add the project root to sys.path if necessary, or ensure pytest runs from the root
# This assumes pytest is run from the project root directory
import encrypt_cli
from modules.cryptography import DEFAULT_PRIVATE_KEY_FILE, DEFAULT_PUBLIC_KEY_FILE
from modules.exceptions.exception import GGBotFatalException


class TestEncryptCLI:
    """Tests for the EncryptCLI class and command-line interactions."""

    # --- Test 'generate-keys' command ---

    @patch("encrypt_cli.KeyManager", autospec=True)
    def test_cli_generate_keys_defaults(self, mock_key_manager_cls):
        """Test 'generate-keys' command with default arguments."""
        mock_key_manager_instance = mock_key_manager_cls.return_value
        mock_key_manager_instance.generate_and_save_keys.return_value = True

        test_args = ["encrypt_cli.py", "generate-keys"]
        with patch.object(sys, "argv", test_args):
            cli = encrypt_cli.EncryptCLI()
            cli.run()

        mock_key_manager_cls.assert_called_once_with(
            DEFAULT_PRIVATE_KEY_FILE, DEFAULT_PUBLIC_KEY_FILE
        )
        mock_key_manager_instance.generate_and_save_keys.assert_called_once_with(
            force_overwrite=False
        )

    @patch("encrypt_cli.KeyManager", autospec=True)
    def test_cli_generate_keys_custom_paths_and_force(self, mock_key_manager_cls):
        """Test 'generate-keys' command with custom paths and --force flag."""
        mock_key_manager_instance = mock_key_manager_cls.return_value
        mock_key_manager_instance.generate_and_save_keys.return_value = True
        custom_priv_path = "keys/my_private.pem"
        custom_pub_path = "keys/my_public.pem"

        test_args = [
            "encrypt_cli.py",
            "generate-keys",
            "--private-key",
            custom_priv_path,
            "--public-key",
            custom_pub_path,
            "--force",
        ]
        with patch.object(sys, "argv", test_args):
            cli = encrypt_cli.EncryptCLI()
            cli.run()

        mock_key_manager_cls.assert_called_once_with(custom_priv_path, custom_pub_path)
        mock_key_manager_instance.generate_and_save_keys.assert_called_once_with(
            force_overwrite=True
        )

    # --- Test 'encrypt' command ---

    @patch("encrypt_cli.EnvFileProcessor", autospec=True)
    @patch("encrypt_cli.EncryptProcessor", autospec=True)
    @patch("encrypt_cli.KeyManager", autospec=True)
    def test_cli_encrypt_defaults(
        self, mock_key_manager_cls, mock_encrypt_processor_cls, mock_env_processor_cls
    ):
        """Test 'encrypt' command with default public key path."""
        mock_key_manager_instance = mock_key_manager_cls.return_value
        mock_public_key = MagicMock()
        mock_key_manager_instance.load_public_key.return_value = mock_public_key
        mock_encryptor_instance = mock_encrypt_processor_cls.return_value
        mock_env_processor_instance = mock_env_processor_cls.return_value
        input_file = "config.env.template"
        output_file = ".env"

        test_args = [
            "encrypt_cli.py",
            "encrypt",
            "--input",
            input_file,
            "--output",
            output_file,
        ]
        with patch.object(sys, "argv", test_args):
            cli = encrypt_cli.EncryptCLI()
            cli.run()

        mock_key_manager_cls.assert_called_once_with(
            public_key_path=DEFAULT_PUBLIC_KEY_FILE
        )
        mock_key_manager_instance.load_public_key.assert_called_once()
        mock_encrypt_processor_cls.assert_called_once_with(mock_public_key)
        mock_env_processor_cls.assert_called_once_with(mock_encryptor_instance)
        mock_env_processor_instance.process_file.assert_called_once_with(
            input_file, output_file
        )

    @patch("encrypt_cli.EnvFileProcessor", autospec=True)
    @patch("encrypt_cli.EncryptProcessor", autospec=True)
    @patch("encrypt_cli.KeyManager", autospec=True)
    def test_cli_encrypt_custom_public_key(
        self, mock_key_manager_cls, mock_encrypt_processor_cls, mock_env_processor_cls
    ):
        """Test 'encrypt' command with a custom public key path."""
        mock_key_manager_instance = mock_key_manager_cls.return_value
        mock_public_key = MagicMock()
        mock_key_manager_instance.load_public_key.return_value = mock_public_key
        mock_encryptor_instance = mock_encrypt_processor_cls.return_value
        mock_env_processor_instance = mock_env_processor_cls.return_value
        input_file = "source.env"
        output_file = "target.env"
        custom_pub_key = "id_rsa.pub"

        test_args = [
            "encrypt_cli.py",
            "encrypt",
            "-i",
            input_file,
            "-o",
            output_file,
            "-k",
            custom_pub_key,
        ]
        with patch.object(sys, "argv", test_args):
            cli = encrypt_cli.EncryptCLI()
            cli.run()

        mock_key_manager_cls.assert_called_once_with(public_key_path=custom_pub_key)
        mock_key_manager_instance.load_public_key.assert_called_once()
        mock_encrypt_processor_cls.assert_called_once_with(mock_public_key)
        mock_env_processor_cls.assert_called_once_with(mock_encryptor_instance)
        mock_env_processor_instance.process_file.assert_called_once_with(
            input_file, output_file
        )

    # --- New Tests for Optional Output and Backup Functionality ---

    @patch("encrypt_cli.EnvFileProcessor", autospec=True)
    @patch("encrypt_cli.EncryptProcessor", autospec=True)
    @patch("encrypt_cli.KeyManager", autospec=True)
    @patch("encrypt_cli.shutil.copy2")
    def test_cli_encrypt_without_output(
        self,
        mock_copy2,
        mock_key_manager_cls,
        mock_encrypt_processor_cls,
        mock_env_processor_cls,
    ):
        """Test 'encrypt' command without output file (should backup input and encrypt in place)."""
        # Setup mocks
        mock_key_manager_instance = mock_key_manager_cls.return_value
        mock_public_key = MagicMock()
        mock_key_manager_instance.load_public_key.return_value = mock_public_key
        mock_encryptor_instance = mock_encrypt_processor_cls.return_value
        mock_env_processor_instance = mock_env_processor_cls.return_value
        input_file = "test.txt"

        # Use patch.object for Path.exists instead of patch decorator
        with patch.object(Path, "exists", return_value=False):
            test_args = [
                "encrypt_cli.py",
                "encrypt",
                "-i",
                input_file,
            ]
            with patch.object(sys, "argv", test_args):
                cli = encrypt_cli.EncryptCLI()
                cli.run()

        # Verify key manager and encrypt processor were called correctly
        mock_key_manager_cls.assert_called_once_with(
            public_key_path=DEFAULT_PUBLIC_KEY_FILE
        )
        mock_key_manager_instance.load_public_key.assert_called_once()
        mock_encrypt_processor_cls.assert_called_once_with(mock_public_key)
        mock_env_processor_cls.assert_called_once_with(mock_encryptor_instance)

        # Verify backup was created
        mock_copy2.assert_called_once_with(Path(input_file), input_file + ".original")

        # Verify input file was used for both input and output
        mock_env_processor_instance.process_file.assert_called_once_with(
            input_file, input_file
        )

    @patch("encrypt_cli.EnvFileProcessor", autospec=True)
    @patch("encrypt_cli.EncryptProcessor", autospec=True)
    @patch("encrypt_cli.KeyManager", autospec=True)
    @patch("encrypt_cli.shutil.copy2")
    def test_cli_encrypt_backup_with_increment(
        self,
        mock_copy2,
        mock_key_manager_cls,
        mock_encrypt_processor_cls,
        mock_env_processor_cls,
    ):
        """Test backup creation with incremental suffix when original backup exists."""
        # Setup mocks
        mock_key_manager_instance = mock_key_manager_cls.return_value
        mock_public_key = MagicMock()
        mock_key_manager_instance.load_public_key.return_value = mock_public_key
        mock_env_processor_instance = mock_env_processor_cls.return_value
        input_file = "test.txt"

        # Define custom mock implementation for Path.exists
        def mock_path_exists(self):
            path_str = str(self)
            if path_str == input_file + ".original":
                return True
            elif path_str == input_file + ".original.1":
                return False
            return False

        with patch.object(Path, "exists", mock_path_exists):
            test_args = [
                "encrypt_cli.py",
                "encrypt",
                "-i",
                input_file,
            ]
            with patch.object(sys, "argv", test_args):
                cli = encrypt_cli.EncryptCLI()
                cli.run()

        # Verify backup was created with .1 suffix
        mock_copy2.assert_called_once_with(Path(input_file), input_file + ".original.1")

        # Verify input file was used for both input and output
        mock_env_processor_instance.process_file.assert_called_once_with(
            input_file, input_file
        )

    # --- Tests for Private Key Parameter ---

    @patch("encrypt_cli.EnvFileProcessor", autospec=True)
    @patch("encrypt_cli.EncryptProcessor", autospec=True)
    @patch("encrypt_cli.KeyManager", autospec=True)
    def test_cli_encrypt_with_private_key_update(
        self, mock_key_manager_cls, mock_encrypt_processor_cls, mock_env_processor_cls
    ):
        """Test setting private key path in the output file."""
        # Setup mocks
        mock_key_manager_instance = mock_key_manager_cls.return_value
        mock_public_key = MagicMock()
        mock_key_manager_instance.load_public_key.return_value = mock_public_key
        input_file = "config.env.template"
        output_file = "config.env"
        private_key_path = "keys/custom_private.pem"

        # Create a spy for the update method instead of replacing it
        with patch("encrypt_cli.EncryptCLI._update_private_key_path") as mock_update:
            with patch.object(Path, "exists", return_value=True):
                test_args = [
                    "encrypt_cli.py",
                    "encrypt",
                    "-i",
                    input_file,
                    "-o",
                    output_file,
                    "--private-key",
                    private_key_path,
                ]
                with patch.object(sys, "argv", test_args):
                    cli = encrypt_cli.EncryptCLI()
                    cli.run()

        # Verify the update method was called
        mock_update.assert_called_once()
        mock_update.assert_called_with(Path(output_file), private_key_path)

    def test_cli_encrypt_update_existing_private_key_path(self):
        """Test updating an existing private key path in the config file."""
        input_file = "config.env"
        private_key_path = "keys/new_private.pem"

        # Create a simulated file content with an existing private key path
        file_content = "CONFIG_VAR=value\nPRIVATE_KEY_PATH=old/path.pem\n"

        # Set up the mock for open
        m = mock_open(read_data=file_content)

        # Spy on the writelines method to capture the actual content
        with patch("builtins.open", m):
            cli = encrypt_cli.EncryptCLI()
            cli._update_private_key_path(Path(input_file), private_key_path)

        # Check the file was opened for reading and writing
        m.assert_any_call(Path(input_file), "r", encoding="utf-8")
        m.assert_any_call(Path(input_file), "w", encoding="utf-8")

        # Check that writelines was called with the updated content
        file_handle = m()
        writelines_calls = file_handle.writelines.call_args_list

        # There should be at least one call to writelines
        assert len(writelines_calls) > 0

        # Get the first call's arguments (the list of lines)
        lines = writelines_calls[0][0][0]

        # Verify the list contains the updated private key path
        updated_line = f"PRIVATE_KEY_PATH={private_key_path}\n"
        assert any(
            line == updated_line for line in lines
        ), f"Expected to find '{updated_line}' in {lines}"

        # Also verify the original CONFIG_VAR is preserved
        assert any(
            "CONFIG_VAR=value" in line for line in lines
        ), "Original content not preserved"

    def test_update_private_key_path_new_simple(self):
        """Simple test for _update_private_key_path method adding a new entry"""
        env_file_path = Path("config.env")
        private_key_path = "keys/private.pem"

        # Create a real string to simulate file content
        file_content = "VAR=value\n"

        # Mock open
        m = mock_open(read_data=file_content)

        # Use writelines method which is what _update_private_key_path uses
        with patch("builtins.open", m):
            cli = encrypt_cli.EncryptCLI()
            cli._update_private_key_path(env_file_path, private_key_path)

        # Check that writelines was called
        file_handle = m()
        writelines_calls = file_handle.writelines.call_args_list

        # There should be exactly one call to writelines
        assert len(writelines_calls) == 1

        # Get the lines that were written
        lines = writelines_calls[0][0][0]

        # The first line should be the original content
        assert (
            lines[0] == "VAR=value\n"
        ), f"Expected first line to be 'VAR=value\\n', got {lines[0]}"

        # There should be a line with the private key path
        expected_key_line = f"PRIVATE_KEY_PATH={private_key_path}\n"
        assert any(
            expected_key_line in line for line in lines
        ), f"Expected to find '{expected_key_line}' in {lines}"

    # --- Test argument parsing errors ---

    def test_cli_instantiation_and_parser_creation(self):
        """Test that CLI initializes and creates a parser."""
        # This test focuses only on the __init__ part
        with patch.object(
            sys, "argv", ["encrypt_cli.py", "generate-keys"]
        ):  # Provide minimal valid args
            cli = encrypt_cli.EncryptCLI()
            assert isinstance(cli.parser, argparse.ArgumentParser)

    # parametrize makes it easy to test multiple scenarios
    @pytest.mark.parametrize(
        "test_args",
        [
            (["encrypt_cli.py"]),  # No command
            (["encrypt_cli.py", "encrypt"]),  # encrypt missing args
            # Note: Removed the test for missing output since it's now optional
            (["encrypt_cli.py", "encrypt", "-o", "out.env"]),  # encrypt missing input
        ],
    )
    def test_cli_missing_required_args(self, test_args):
        """Test that argparse raises SystemExit if required args are missing."""
        with patch.object(sys, "argv", test_args):
            # Need to catch the SystemExit raised by argparse during parse_args()
            # which happens inside the CLI's run() method.
            with pytest.raises(SystemExit) as e:
                # Instantiate the CLI first
                cli = encrypt_cli.EncryptCLI()
                # Call run() to trigger parse_args()
                cli.run()
            assert e.type is SystemExit  # Check it's the expected exception

    # --- Test failure paths ---

    @patch("encrypt_cli.KeyManager", autospec=True)
    def test_cli_generate_keys_failure(self, mock_key_manager_cls):
        """Test CLI behavior when KeyManager.generate_and_save_keys returns False."""
        mock_key_manager_instance = mock_key_manager_cls.return_value
        # Simulate failure (e.g., user aborted overwrite)
        mock_key_manager_instance.generate_and_save_keys.return_value = False

        test_args = ["encrypt_cli.py", "generate-keys"]
        with patch.object(sys, "argv", test_args):
            cli = encrypt_cli.EncryptCLI()
            # We expect run() to complete without error, but the underlying action didn't fully succeed.
            # The logging in KeyManager should indicate the abortion.
            cli.run()

        mock_key_manager_cls.assert_called_once()
        mock_key_manager_instance.generate_and_save_keys.assert_called_once_with(
            force_overwrite=False
        )
        # No specific CLI output to check here, relies on KeyManager logging.

    @patch("encrypt_cli.KeyManager", autospec=True)
    def test_cli_encrypt_key_load_failure(self, mock_key_manager_cls):
        """Test CLI behavior when KeyManager.load_public_key fails."""
        mock_key_manager_instance = mock_key_manager_cls.return_value
        # Simulate failure (e.g., file not found, invalid format)
        mock_key_manager_instance.load_public_key.side_effect = GGBotFatalException(
            "Test key load error"
        )

        test_args = ["encrypt_cli.py", "encrypt", "-i", "in.env", "-o", "out.env"]
        with patch.object(sys, "argv", test_args):
            cli = encrypt_cli.EncryptCLI()
            # Expect the exception from KeyManager to propagate
            with pytest.raises(GGBotFatalException) as exc_info:
                cli.run()
            assert "Test key load error" in str(exc_info.value)

        mock_key_manager_cls.assert_called_once()
        mock_key_manager_instance.load_public_key.assert_called_once()

    # --- Test helper methods ---

    def test_backup_input_file(self):
        """Test the _backup_input_file method creates a backup with correct naming."""
        input_path = Path("test.txt")

        # Test case 1: No backup exists yet
        with patch.object(Path, "exists") as mock_exists:
            mock_exists.return_value = False
            with patch("encrypt_cli.shutil.copy2") as mock_copy2:
                cli = encrypt_cli.EncryptCLI()
                result = cli._backup_input_file(input_path)

                mock_copy2.assert_called_once_with(input_path, "test.txt.original")
                assert str(result) == "test.txt.original"

        # Test case 2: First backup exists, should use increment
        with patch.object(Path, "exists") as mock_exists:
            # Return True for first check, False for second
            mock_exists.side_effect = [True, False]
            with patch("encrypt_cli.shutil.copy2") as mock_copy2:
                cli = encrypt_cli.EncryptCLI()
                result = cli._backup_input_file(input_path)

                mock_copy2.assert_called_once_with(input_path, "test.txt.original.1")
                assert str(result) == "test.txt.original.1"

    # Note: Testing failures within EnvFileProcessor (like file IO errors)
    # would require patching EnvFileProcessor.process_file to raise an exception
    # or mocking Path operations, which adds significant complexity.
    # The current tests focus on failures in KeyManager interactions.
