import os
import pytest
from unittest.mock import patch
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import logging

from modules.cryptography.key_manager import KeyManager
from modules.exceptions.exception import GGBotFatalException


@pytest.fixture
def key_manager_fixture(tmp_path):
    """Fixture providing a KeyManager instance using tmp_path."""
    private_key_path = tmp_path / "test_private.pem"
    public_key_path = tmp_path / "test_public.pem"
    # Renamed fixture to avoid potential pytest name collision if class uses 'key_manager' attribute
    return KeyManager(str(private_key_path), str(public_key_path))


class TestKeyManager:
    """Tests for the KeyManager class."""

    def test_key_generation_success(self, key_manager_fixture: KeyManager, tmp_path):
        """Test successful generation and saving of keys."""
        key_manager = key_manager_fixture  # Get instance from fixture
        private_key_path = key_manager.private_key_path
        public_key_path = key_manager.public_key_path

        assert not private_key_path.exists()
        assert not public_key_path.exists()

        result = key_manager.generate_and_save_keys(force_overwrite=True)

        assert result is True
        assert private_key_path.exists()
        assert public_key_path.exists()

        # Check private key permissions (stat().st_mode & 0o777 gives permissions)
        if os.name != "nt":  # Skip permission check on Windows
            assert (private_key_path.stat().st_mode & 0o777) == 0o600

        # Try loading them to verify format
        try:
            with open(public_key_path, "rb") as f:
                pub_key_loaded = serialization.load_pem_public_key(f.read())
            assert isinstance(pub_key_loaded, rsa.RSAPublicKey)

            with open(private_key_path, "rb") as f:
                priv_key_loaded = serialization.load_pem_private_key(
                    f.read(), password=None
                )
            assert isinstance(priv_key_loaded, rsa.RSAPrivateKey)
        except Exception as e:
            pytest.fail(f"Failed to load generated keys: {e}")

    @patch("rich.prompt.Confirm.ask", return_value=False)  # Mock user saying 'no'
    def test_key_generation_abort_on_existing(
        self, mock_confirm_ask, key_manager_fixture: KeyManager, tmp_path
    ):
        """Test that generation aborts if keys exist and user doesn't force."""
        key_manager = key_manager_fixture
        private_key_path = key_manager.private_key_path
        public_key_path = key_manager.public_key_path

        # Create dummy files
        private_key_path.touch()
        public_key_path.touch()

        result = key_manager.generate_and_save_keys(force_overwrite=False)

        assert result is False
        mock_confirm_ask.assert_called_once()  # Ensure prompt was shown

    @patch("rich.prompt.Confirm.ask")  # Mock to prevent actual prompt
    def test_key_generation_force_overwrite(
        self, mock_confirm_ask, key_manager_fixture: KeyManager, tmp_path
    ):
        """Test that generation proceeds with force=True even if keys exist."""
        key_manager = key_manager_fixture
        private_key_path = key_manager.private_key_path
        public_key_path = key_manager.public_key_path

        # Create dummy files with some content
        private_key_path.write_text("old_private")
        public_key_path.write_text("old_public")
        old_priv_mtime = private_key_path.stat().st_mtime
        old_pub_mtime = public_key_path.stat().st_mtime

        result = key_manager.generate_and_save_keys(force_overwrite=True)

        assert result is True
        mock_confirm_ask.assert_not_called()  # Ensure prompt was skipped
        assert private_key_path.exists()
        assert public_key_path.exists()
        # Check content is not the dummy content (implicitly checks overwrite)
        assert private_key_path.read_text() != "old_private"
        assert public_key_path.read_text() != "old_public"
        # Check modification time changed (files were overwritten)
        assert private_key_path.stat().st_mtime != old_priv_mtime
        assert public_key_path.stat().st_mtime != old_pub_mtime

    def test_load_public_key_success(self, key_manager_fixture: KeyManager):
        """Test loading a valid public key."""
        key_manager = key_manager_fixture
        # First generate keys
        key_manager.generate_and_save_keys(force_overwrite=True)

        # Reset internal state to force loading from file
        key_manager._public_key = None

        try:
            loaded_key = key_manager.load_public_key()
            assert isinstance(loaded_key, rsa.RSAPublicKey)
            # Check caching
            assert key_manager._public_key is loaded_key
            # Call again, should return cached key
            assert key_manager.load_public_key() is loaded_key
        except Exception as e:
            pytest.fail(f"load_public_key failed: {e}")

    def test_load_public_key_file_not_found(
        self, key_manager_fixture: KeyManager, tmp_path
    ):
        """Test loading public key when file doesn't exist."""
        key_manager = key_manager_fixture
        # Ensure file does not exist
        assert not key_manager.public_key_path.exists()

        with pytest.raises(GGBotFatalException) as exc_info:
            key_manager.load_public_key()
        assert "No such file or directory" in str(exc_info.value)

    def test_load_public_key_invalid_format(
        self, key_manager_fixture: KeyManager, tmp_path
    ):
        """Test loading a file that is not a valid public key."""
        key_manager = key_manager_fixture
        public_key_path = key_manager.public_key_path
        public_key_path.write_text("this is not a pem key")

        with pytest.raises(GGBotFatalException) as exc_info:
            key_manager.load_public_key()
        # Error message might vary, check it's load-related
        assert "Unable to load PEM file." in str(
            exc_info.value
        ) and "MalformedFraming" in str(exc_info.value)

    # --- Tests for load_private_key ---

    def test_load_private_key_success(self, key_manager_fixture: KeyManager):
        """Test loading a valid private key."""
        key_manager = key_manager_fixture
        # First generate keys to ensure the private key file exists and is valid
        key_manager.generate_and_save_keys(force_overwrite=True)

        # Reset internal state to force loading from file
        key_manager._private_key = None

        try:
            loaded_key = key_manager.load_private_key()
            assert isinstance(loaded_key, rsa.RSAPrivateKey)
            # Check caching
            assert key_manager._private_key is loaded_key
            # Call again, should return cached key
            assert key_manager.load_private_key() is loaded_key
        except Exception as e:
            pytest.fail(f"load_private_key failed: {e}")

    def test_load_private_key_file_not_found(self, key_manager_fixture: KeyManager):
        """Test loading private key when file doesn't exist."""
        key_manager = key_manager_fixture
        assert not key_manager.private_key_path.exists()
        with pytest.raises(GGBotFatalException, match="Private key file not found"):
            key_manager.load_private_key()

    @pytest.mark.skipif(
        os.name == "nt", reason="Permission tests unreliable on Windows"
    )
    def test_load_private_key_bad_permissions(
        self, key_manager_fixture: KeyManager, tmp_path, caplog
    ):
        """Test loading private key with insecure permissions (non-Windows)."""
        key_manager = key_manager_fixture
        key_manager.generate_and_save_keys(force_overwrite=True)
        private_key_path = key_manager.private_key_path

        # Set bad permissions (e.g., 644)
        private_key_path.chmod(0o644)

        # Reset internal state
        key_manager._private_key = None

        # Should load successfully but log a warning
        with caplog.at_level(logging.WARNING):
            try:
                key_manager.load_private_key()
            except Exception as e:
                pytest.fail(f"load_private_key failed unexpectedly: {e}")

        assert (
            f"Warning: Private key file {private_key_path} has insecure permissions (0o644)"
            in caplog.text
        )
        assert key_manager._private_key is not None  # Check it loaded

        # Set group write permission (should also warn)
        private_key_path.chmod(0o620)
        key_manager._private_key = None
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            key_manager.load_private_key()
        assert (
            f"Warning: Private key file {private_key_path} has insecure permissions (0o620)"
            in caplog.text
        )
        assert key_manager._private_key is not None

    def test_load_private_key_invalid_format(
        self, key_manager_fixture: KeyManager, tmp_path
    ):
        """Test loading a file that is not a valid private key."""
        key_manager = key_manager_fixture
        private_key_path = key_manager.private_key_path
        private_key_path.write_text("this is not a pem private key")

        with pytest.raises(
            GGBotFatalException, match="Invalid private key format/type"
        ):
            key_manager.load_private_key()

    # Test for PermissionError would require more complex setup (e.g., creating file as different user)
    # or potentially mocking os.chmod/Path.stat, which might be overly complex for this stage.
