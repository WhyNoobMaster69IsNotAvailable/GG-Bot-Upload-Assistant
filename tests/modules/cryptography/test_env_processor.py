import pytest
from unittest.mock import MagicMock, call
from pathlib import Path

from modules.cryptography import ENCRYPTION_MARKER
from modules.cryptography.env_processor import EnvFileProcessor
from modules.cryptography.encrypt_decrypt_processor import EncryptProcessor


# --- Fixtures defined outside the class ---


# Mock EncryptProcessor fixture
@pytest.fixture
def mock_encryptor_fixture():
    """Fixture providing a mocked EncryptProcessor."""
    mock = MagicMock(spec=EncryptProcessor)

    def _mock_encrypt(value: str):
        if value == "too_long_value":  # Simulate failure/skip for a specific value
            return None
        elif value == "":  # Simulate empty value handling
            return ""
        else:
            # Simple mock encryption, clearly indicating input
            return f"encrypted_{value.replace(' ', '_').replace('#', '_')}"  # Make it path/log safe

    mock.encrypt.side_effect = _mock_encrypt
    return mock


@pytest.fixture
def env_processor_fixture(mock_encryptor_fixture):
    """Fixture providing an EnvFileProcessor instance with a mocked encryptor."""
    return EnvFileProcessor(mock_encryptor_fixture)


# Sample input .env content (defined once)
SAMPLE_ENV_CONTENT = f"""
# This is a comment
BLANK_LINE=
NORMAL_VAR=value1

SECRET_KEY=secret_value {ENCRYPTION_MARKER}
ANOTHER_SECRET="quoted secret" {ENCRYPTION_MARKER}
EMPTY_SECRET= {ENCRYPTION_MARKER}
EMPTY_QUOTED_SECRET="" {ENCRYPTION_MARKER}
TOO_LONG_SECRET=too_long_value {ENCRYPTION_MARKER}

VAR_WITH_MARKER_TEXT=some value # ENCRYPT me please {ENCRYPTION_MARKER}

# Invalid key marker
#=invalid_key_format {ENCRYPTION_MARKER}
 = space_key {ENCRYPTION_MARKER}

NO_MARKER=dont_touch_me
"""

# Expected output content based on SAMPLE_ENV_CONTENT and mock_encryptor
EXPECTED_ENV_OUTPUT = f"""
# This is a comment
BLANK_LINE=
NORMAL_VAR=value1

SECRET_KEY=ENC::encrypted_secret_value
ANOTHER_SECRET=ENC::encrypted_quoted_secret
EMPTY_SECRET=
EMPTY_QUOTED_SECRET=
TOO_LONG_SECRET=too_long_value

VAR_WITH_MARKER_TEXT=ENC::encrypted_some_value___ENCRYPT_me_please

# Invalid key marker
#=invalid_key_format {ENCRYPTION_MARKER}
 = space_key {ENCRYPTION_MARKER}

NO_MARKER=dont_touch_me
"""


class TestEnvProcessor:
    """Tests for the EnvFileProcessor class."""

    def test_process_file_success(
        self,
        env_processor_fixture: EnvFileProcessor,
        mock_encryptor_fixture: MagicMock,
        tmp_path: Path,
    ):
        """Test processing a valid .env file."""
        env_processor = env_processor_fixture
        mock_encryptor = mock_encryptor_fixture
        input_file = tmp_path / "input.env"
        output_file = tmp_path / "output.env"
        input_file.write_text(SAMPLE_ENV_CONTENT, encoding="utf-8")

        env_processor.process_file(str(input_file), str(output_file))

        assert output_file.exists()
        actual_output = output_file.read_text(encoding="utf-8")

        # Normalize line endings and compare line by line for easier debugging
        expected_lines = [
            line.strip() for line in EXPECTED_ENV_OUTPUT.strip().splitlines()
        ]
        actual_lines = [line.strip() for line in actual_output.strip().splitlines()]
        assert actual_lines == expected_lines

        # Verify calls to the mock encryptor (only for valid keys)
        expected_calls = [
            call("secret_value"),
            call("quoted secret"),
            # Empty values are handled before calling encrypt
            call("too_long_value"),  # This one returns None in our mock
            call("some value # ENCRYPT me please"),
        ]
        mock_encryptor.encrypt.assert_has_calls(expected_calls, any_order=False)
        # Check total number of calls
        assert mock_encryptor.encrypt.call_count == len(expected_calls)

    def test_process_file_input_not_found(
        self, env_processor_fixture: EnvFileProcessor, tmp_path: Path
    ):
        """Test processing when the input file doesn't exist."""
        env_processor = env_processor_fixture
        input_file = tmp_path / "non_existent.env"
        output_file = tmp_path / "output.env"

        with pytest.raises(SystemExit):  # EnvProcessor calls sys.exit(1)
            env_processor.process_file(str(input_file), str(output_file))

    def test_process_empty_input_file(
        self,
        env_processor_fixture: EnvFileProcessor,
        mock_encryptor_fixture: MagicMock,
        tmp_path: Path,
    ):
        """Test processing an empty input file."""
        env_processor = env_processor_fixture
        mock_encryptor = mock_encryptor_fixture
        input_file = tmp_path / "empty.env"
        output_file = tmp_path / "output.env"
        input_file.touch()  # Create empty file

        env_processor.process_file(str(input_file), str(output_file))

        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == ""
        mock_encryptor.encrypt.assert_not_called()  # No encryption should happen

    def test_process_file_various_formats(
        self,
        env_processor_fixture: EnvFileProcessor,
        mock_encryptor_fixture: MagicMock,
        tmp_path: Path,
    ):
        """Test processing file with variations in spacing and non-marker comments."""
        env_processor = env_processor_fixture
        mock_encryptor = mock_encryptor_fixture
        input_file = tmp_path / "formats.env"
        output_file = tmp_path / "output.env"

        input_content = f"""
KEY1=value1 {ENCRYPTION_MARKER}
KEY2 = value2 {ENCRYPTION_MARKER}
KEY3   =    value3    {ENCRYPTION_MARKER}
# KEY4=commented out {ENCRYPTION_MARKER}
KEY5="  spaced value  " {ENCRYPTION_MARKER}
KEY6=contains # ENCRYPT but not marker
KEY7=ends with space {ENCRYPTION_MARKER}
"""
        # Expected output based on refined logic and mock encryptor
        expected_output_content = f"""
KEY1=ENC::encrypted_value1
KEY2=ENC::encrypted_value2
KEY3=ENC::encrypted_value3
# KEY4=commented out {ENCRYPTION_MARKER}
KEY5=ENC::encrypted___spaced_value__
KEY6=contains # ENCRYPT but not marker
KEY7=ENC::encrypted_ends_with_space
"""
        input_file.write_text(input_content, encoding="utf-8")

        env_processor.process_file(str(input_file), str(output_file))

        assert output_file.exists()
        actual_output = output_file.read_text(encoding="utf-8")
        # Normalize
        expected_lines = [
            line.strip() for line in expected_output_content.strip().splitlines()
        ]
        actual_lines = [line.strip() for line in actual_output.strip().splitlines()]
        assert actual_lines == expected_lines

        # Verify calls (KEY4 is commented out, so no call; KEY6 doesn't end with marker)
        expected_calls = [
            call("value1"),
            call("value2"),
            call("value3"),
            call("  spaced value  "),
            call("ends with space"),
        ]
        mock_encryptor.encrypt.assert_has_calls(expected_calls, any_order=True)
        assert mock_encryptor.encrypt.call_count == len(expected_calls)
