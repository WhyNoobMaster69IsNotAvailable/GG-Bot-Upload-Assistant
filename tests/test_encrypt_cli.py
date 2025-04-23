import pytest
from unittest.mock import patch, MagicMock
import sys
import argparse  # Import needed for isinstance check

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
            (["encrypt_cli.py", "encrypt", "-i", "in.env"]),  # encrypt missing output
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

    # Note: Testing failures within EnvFileProcessor (like file IO errors)
    # would require patching EnvFileProcessor.process_file to raise an exception
    # or mocking Path operations, which adds significant complexity.
    # The current tests focus on failures in KeyManager interactions.
