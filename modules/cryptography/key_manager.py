# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
import os
from pathlib import Path
from typing import Optional
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from rich.prompt import Confirm

from modules.cryptography import DEFAULT_PRIVATE_KEY_FILE, DEFAULT_PUBLIC_KEY_FILE
from modules.exceptions.exception import GGBotFatalException


class KeyManager:
    """Handles generation, loading, and saving of RSA key pairs."""

    def __init__(
        self,
        private_key_path: str = DEFAULT_PRIVATE_KEY_FILE,
        public_key_path: str = DEFAULT_PUBLIC_KEY_FILE,
    ):
        self.private_key_path = Path(private_key_path)
        self.public_key_path = Path(public_key_path)
        self._private_key: Optional[rsa.RSAPrivateKey] = None
        self._public_key: Optional[rsa.RSAPublicKey] = None

    def generate_and_save_keys(self, force_overwrite: bool = False):
        """Generates and saves a new RSA key pair."""
        logging.info("[KeyManager] Generating new secret key pair...")
        if not force_overwrite and (
            self.private_key_path.exists() or self.public_key_path.exists()
        ):
            confirm = Confirm.ask(
                f"Warning: Key file(s) '{self.private_key_path.name}' or '{self.public_key_path.name}' already exist "
                f"in directory '{self.private_key_path.parent}'.\nOverwrite? (y/N): ",
                default="n",
            )
            if not confirm:
                logging.info("[KeyManager] Key generation aborted by user.")
                return False  # Indicate abortion

        logging.info("[KeyManager] Generating RSA key pair (4096 bits)...")
        self._private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=4096, backend=default_backend()
        )
        self._public_key = self._private_key.public_key()

        # Ensure directories exist
        self.private_key_path.parent.mkdir(parents=True, exist_ok=True)
        self.public_key_path.parent.mkdir(parents=True, exist_ok=True)

        self._save_private_key()
        self._save_public_key()
        logging.info("[KeyManager] Key pair generated and saved successfully.")
        return True  # Indicate success

    def _save_private_key(self):
        """Saves the private key to its designated path."""
        if not self._private_key:
            logging.error("[KeyManager] No private key available to save.")
            return

        logging.info(f"[KeyManager] Saving private key to {self.private_key_path}")
        pem_private = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        try:
            with open(self.private_key_path, "wb") as f:
                f.write(pem_private)
            # Set restrictive permissions (owner read/write only)
            os.chmod(self.private_key_path, 0o600)
            logging.info("[KeyManager] Private key saved. Permissions set to 600.")
        except OSError as e:
            logging.error(
                f"[KeyManager] Error saving or setting permissions for private key {self.private_key_path}: {e}"
            )
            raise GGBotFatalException(e)

    def _save_public_key(self):
        """Saves the public key to its designated path."""
        if not self._public_key:
            logging.error("[KeyManager] No public key available to save.")
            return

        logging.info(f"[KeyManager] Saving public key to {self.public_key_path}")
        pem_public = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        try:
            with open(self.public_key_path, "wb") as f:
                f.write(pem_public)
            logging.info("[KeyManager] Public key saved.")
        except OSError as e:
            logging.error(
                f"[KeyManager] Error saving public key {self.public_key_path}: {e}"
            )
            raise GGBotFatalException(e)

    def load_public_key(self) -> rsa.RSAPublicKey:
        """Loads the public key from its designated path."""
        if self._public_key:
            return self._public_key

        logging.info(f"[KeyManager] Loading public key from {self.public_key_path}...")
        try:
            with open(self.public_key_path, "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(), backend=default_backend()
                )
            if not isinstance(public_key, rsa.RSAPublicKey):
                # This check might be redundant with load_pem_public_key typing
                raise TypeError("[KeyManager] Key loaded is not an RSA public key.")
            self._public_key = public_key

            logging.info("[KeyManager] Public key loaded successfully.")
            return self._public_key
        except FileNotFoundError as e:
            logging.error(
                f"[KeyManager] Error: Public key file not found at {self.public_key_path}"
            )
            raise GGBotFatalException(e)
        except (TypeError, ValueError, Exception) as e:
            logging.error(f"Error loading public key: {e}")
            raise GGBotFatalException(e)

    def load_private_key(self) -> rsa.RSAPrivateKey:
        """Loads the private key from its designated path."""
        # Note: This assumes the private key is NOT password protected.
        # If it could be, password handling would need to be added here.
        if self._private_key:
            return self._private_key

        logging.info(
            f"[KeyManager] Loading private key from {self.private_key_path}..."
        )
        if not self.private_key_path.exists():
            logging.error(
                f"[KeyManager] Error: Private key file not found at {self.private_key_path}"
            )
            raise GGBotFatalException(
                f"Private key file not found: {self.private_key_path}"
            )

        try:
            # Check permissions before reading (basic check, might not work perfectly on all OS/filesystems)
            if os.name != "nt":  # Skip permission check on Windows
                perms = self.private_key_path.stat().st_mode & 0o777
                if perms & 0o077:  # Check if group/other has any permissions
                    logging.warning(
                        f"[KeyManager] Warning: Private key file {self.private_key_path} has insecure permissions ({oct(perms)}). Should be 600 or 400."
                    )
                    # Depending on policy, you might raise an error here instead of just warning.

            with open(self.private_key_path, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,  # No password
                    backend=default_backend(),
                )
            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise TypeError("[KeyManager] Key loaded is not an RSA private key.")
            self._private_key = private_key

            logging.info("[KeyManager] Private key loaded successfully.")
            return self._private_key
        except (
            FileNotFoundError
        ) as e:  # Should be caught by exists() check, but belt-and-suspenders
            logging.error(
                f"[KeyManager] Error: Private key file not found at {self.private_key_path}"
            )
            raise GGBotFatalException(e)
        except PermissionError as e:
            logging.error(
                f"[KeyManager] Error: Permission denied reading private key file {self.private_key_path}"
            )
            raise GGBotFatalException(e)
        except (TypeError, ValueError) as e:
            # Catches incorrect key types, format errors, potentially unsupported crypto
            logging.error(
                f"[KeyManager] Error loading private key: Invalid format or type. {e}"
            )
            raise GGBotFatalException(f"Invalid private key format/type: {e}")
        except Exception as e:  # Catch any other loading errors
            logging.exception(
                f"[KeyManager] An unexpected error occurred loading private key: {e}"
            )
            raise GGBotFatalException(f"Unexpected error loading private key: {e}")
