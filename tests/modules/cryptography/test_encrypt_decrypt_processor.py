import pytest
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding  # alias
from typing import Optional

from modules.cryptography.encrypt_decrypt_processor import (
    EncryptProcessor,
    DecryptProcessor,
)


# --- Fixtures defined outside the class ---


# Fixture to generate a key pair for testing encryption
# Scope='session' makes it run once for all tests in the session
@pytest.fixture(scope="session")
def test_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )  # 2048 is faster for tests
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.fixture
def encrypt_processor_fixture(test_rsa_key_pair):
    """Fixture providing an EncryptProcessor instance."""
    _, public_key = test_rsa_key_pair
    return EncryptProcessor(public_key)


@pytest.fixture
def decrypt_key_fixture(test_rsa_key_pair):
    """Fixture providing a helper function to decrypt using the private key."""
    private_key, _ = test_rsa_key_pair
    padding_instance = asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )

    def _decrypt(encrypted_b64_str: str) -> str:
        encrypted_bytes = base64.b64decode(encrypted_b64_str.encode("utf-8"))
        decrypted_bytes = private_key.decrypt(encrypted_bytes, padding_instance)
        return decrypted_bytes.decode("utf-8")

    return _decrypt


class TestEncryptProcessor:
    """Tests for the EncryptProcessor class."""

    def test_encrypt_valid_string(
        self, encrypt_processor_fixture: EncryptProcessor, decrypt_key_fixture
    ):
        """Test encrypting a normal string."""
        encrypt_processor = encrypt_processor_fixture
        decrypt_key = decrypt_key_fixture
        original_value = "This is a secret message."
        encrypted_value = encrypt_processor.encrypt(original_value)

        assert encrypted_value is not None
        assert isinstance(encrypted_value, str)
        # Check if it's valid base64
        try:
            base64.b64decode(encrypted_value.encode("utf-8"))
        except Exception:
            pytest.fail("Encrypted value is not valid base64")

        # Decrypt to verify content
        decrypted_value = decrypt_key(encrypted_value)
        assert decrypted_value == original_value

    def test_encrypt_empty_string(self, encrypt_processor_fixture: EncryptProcessor):
        """Test encrypting an empty string."""
        encrypt_processor = encrypt_processor_fixture
        original_value = ""
        encrypted_value = encrypt_processor.encrypt(original_value)
        assert encrypted_value == ""

    def test_encrypt_string_too_long(self, encrypt_processor_fixture: EncryptProcessor):
        """Test encrypting a string that exceeds the maximum length."""
        encrypt_processor = encrypt_processor_fixture
        # Max length depends on key size (2048 bits = 256 bytes) and padding (OAEP/SHA256 uses 2*32+2=66 bytes)
        # max_len = 256 - 66 = 190 bytes for 2048 key
        max_len = encrypt_processor.max_plaintext_len
        long_value = "a" * (max_len + 1)

        encrypted_value = encrypt_processor.encrypt(long_value)
        assert encrypted_value is None

    def test_encrypt_max_length_string(
        self, encrypt_processor_fixture: EncryptProcessor, decrypt_key_fixture
    ):
        """Test encrypting a string that is exactly the maximum length."""
        encrypt_processor = encrypt_processor_fixture
        decrypt_key = decrypt_key_fixture
        max_len = encrypt_processor.max_plaintext_len
        max_value = "a" * max_len

        encrypted_value = encrypt_processor.encrypt(max_value)
        assert encrypted_value is not None

        # Decrypt to verify
        decrypted_value = decrypt_key(encrypted_value)
        assert decrypted_value == max_value

    def test_encrypt_utf8_string(
        self, encrypt_processor_fixture: EncryptProcessor, decrypt_key_fixture
    ):
        """Test encrypting a string with UTF-8 characters."""
        encrypt_processor = encrypt_processor_fixture
        decrypt_key = decrypt_key_fixture
        original_value = "你好, 世界! €ảm ơn"
        encrypted_value = encrypt_processor.encrypt(original_value)

        assert encrypted_value is not None
        assert isinstance(encrypted_value, str)

        # Decrypt to verify content
        decrypted_value = decrypt_key(encrypted_value)
        assert decrypted_value == original_value


# --- Tests for DecryptProcessor ---


@pytest.fixture
def decrypt_processor_fixture(test_rsa_key_pair):
    """Fixture providing a DecryptProcessor instance."""
    private_key, _ = test_rsa_key_pair
    return DecryptProcessor(private_key)


@pytest.fixture
def encrypt_key_fixture(test_rsa_key_pair):
    """Fixture providing a helper function to encrypt using the public key."""
    _, public_key = test_rsa_key_pair
    padding_instance = asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )

    def _encrypt(value: str) -> Optional[str]:
        if not value:
            return ""
        value_bytes = value.encode("utf-8")
        # Assume length check is okay for test values
        try:
            encrypted_bytes = public_key.encrypt(value_bytes, padding_instance)
            return base64.b64encode(encrypted_bytes).decode("utf-8")
        except Exception:
            return None

    return _encrypt


class TestDecryptProcessor:
    """Tests for the DecryptProcessor class."""

    def test_decrypt_valid_string(
        self, decrypt_processor_fixture: DecryptProcessor, encrypt_key_fixture
    ):
        """Test decrypting a valid base64 encoded encrypted string."""
        decryptor = decrypt_processor_fixture
        encrypt = encrypt_key_fixture
        original_value = "This should be decrypted correctly."
        encrypted_value = encrypt(original_value)
        assert encrypted_value is not None

        decrypted_value = decryptor.decrypt(encrypted_value)
        assert decrypted_value == original_value

    def test_decrypt_utf8_string(
        self, decrypt_processor_fixture: DecryptProcessor, encrypt_key_fixture
    ):
        """Test decrypting a string containing UTF-8 characters."""
        decryptor = decrypt_processor_fixture
        encrypt = encrypt_key_fixture
        original_value = "Decryption: 你好, 世界! €ảm ơn"
        encrypted_value = encrypt(original_value)
        assert encrypted_value is not None

        decrypted_value = decryptor.decrypt(encrypted_value)
        assert decrypted_value == original_value

    def test_decrypt_empty_string(self, decrypt_processor_fixture: DecryptProcessor):
        """Test decrypting an empty string (should return empty string)."""
        decryptor = decrypt_processor_fixture
        decrypted_value = decryptor.decrypt("")
        assert decrypted_value == ""

    def test_decrypt_invalid_base64(self, decrypt_processor_fixture: DecryptProcessor):
        """Test decrypting a string that is not valid base64."""
        decryptor = decrypt_processor_fixture
        invalid_b64 = "this is not base64!@#$"
        decrypted_value = decryptor.decrypt(invalid_b64)
        assert decrypted_value is None

    def test_decrypt_invalid_ciphertext(
        self, decrypt_processor_fixture: DecryptProcessor
    ):
        """Test decrypting valid base64 that isn't valid ciphertext (or wrong key)."""
        decryptor = decrypt_processor_fixture
        # Valid base64, but unlikely to be valid RSA-OAEP ciphertext
        random_b64 = base64.b64encode(b"just some random bytes").decode("utf-8")
        decrypted_value = decryptor.decrypt(random_b64)
        assert decrypted_value is None

    def test_decrypt_with_different_key(
        self, decrypt_processor_fixture: DecryptProcessor, encrypt_key_fixture
    ):
        """Test decrypting with the wrong private key (simulated by re-encrypting)."""
        decryptor = decrypt_processor_fixture
        # Generate a completely separate key pair
        wrong_private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048
        )
        wrong_public_key = wrong_private_key.public_key()
        padding_instance = asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )

        # Encrypt with the WRONG public key
        original_value = "Encrypted with wrong key"
        value_bytes = original_value.encode("utf-8")
        encrypted_bytes_wrong = wrong_public_key.encrypt(value_bytes, padding_instance)
        encrypted_b64_wrong = base64.b64encode(encrypted_bytes_wrong).decode("utf-8")

        # Attempt to decrypt with the CORRECT private key (from fixture)
        decrypted_value = decryptor.decrypt(encrypted_b64_wrong)
        assert decrypted_value is None
