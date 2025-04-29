import base64
import logging
from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class EncryptProcessor:
    """Encrypts string values using an RSA public key."""

    def __init__(self, public_key: rsa.RSAPublicKey):
        self.public_key = public_key
        self.key_size_bytes = self.public_key.key_size // 8
        # Using SHA256, hash length is 32 bytes
        sha256_hash_len = 32
        # Max length = key_size_bytes - 2 * hash_length_bytes - 2
        self.max_plaintext_len = self.key_size_bytes - 2 * sha256_hash_len - 2
        self.padding = padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )

    def encrypt(self, value: str) -> Optional[str]:
        """
        Encrypts a string value using the public key.

        Returns:
            Base64 encoded ciphertext as a string, or None if encryption failed or skipped.
        """
        # Early return for empty input
        if not value:
            return ""

        value_bytes = value.encode("utf-8")

        # Early return if value is too long
        if len(value_bytes) > self.max_plaintext_len:
            logging.warning(
                f"[EncryptProcessor] Value length ({len(value_bytes)} bytes) "
                f"exceeds maximum ({self.max_plaintext_len} bytes) "
                f"for RSA-OAEP with SHA256 padding and this key size. Skipping encryption."
            )
            return None  # Indicate skip/failure

        # Main encryption logic
        try:
            encrypted_bytes = self.public_key.encrypt(value_bytes, self.padding)
            return base64.b64encode(encrypted_bytes).decode("utf-8")
        except Exception as e:
            logging.error(f"[EncryptProcessor] Encryption failed: {e}")
            return None  # Indicate skip/failure


class DecryptProcessor:
    """Decrypts base64 encoded ciphertext using an RSA private key."""

    def __init__(self, private_key: rsa.RSAPrivateKey):
        self.private_key = private_key
        # Use the same padding scheme as encryption
        self.padding = padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )

    def decrypt(self, encrypted_b64_str: str) -> Optional[str]:
        """
        Decrypts a base64 encoded ciphertext string.

        Args:
            encrypted_b64_str: The base64 encoded ciphertext (WITHOUT the 'ENC::' prefix).

        Returns:
            The decrypted string, or None if decryption fails.
        """
        if not encrypted_b64_str:
            logging.warning("[DecryptProcessor] Received empty string for decryption.")
            return ""  # Consistent with encrypting empty string

        try:
            encrypted_bytes = base64.b64decode(encrypted_b64_str.encode("utf-8"))
        except (ValueError, TypeError) as e:
            logging.error(
                f"[DecryptProcessor] Failed to decode base64: {e}. Input: '{encrypted_b64_str[:20]}...'"
            )
            return None

        try:
            decrypted_bytes = self.private_key.decrypt(encrypted_bytes, self.padding)
            return decrypted_bytes.decode("utf-8")
        except ValueError as e:
            # Catches various issues like decryption error, incorrect key, potentially size issues
            logging.error(
                f"[DecryptProcessor] Decryption failed (ValueError): {e}. Check if the correct private key is used and data is not corrupted."
            )
            return None
        except Exception as e:
            # Catch any other unexpected crypto errors
            logging.exception(
                f"[DecryptProcessor] An unexpected error occurred during decryption: {e}"
            )
            return None
