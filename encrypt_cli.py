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

import argparse
import logging
import shutil
from pathlib import Path

from modules.cryptography import (
    ENCRYPTION_MARKER,
    DEFAULT_PRIVATE_KEY_FILE,
    DEFAULT_PUBLIC_KEY_FILE,
)
from modules.cryptography.encrypt_decrypt_processor import EncryptProcessor
from modules.cryptography.env_processor import EnvFileProcessor
from modules.cryptography.key_manager import KeyManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class EncryptCLI:
    """Handles command-line interface operations."""

    def __init__(self):
        self.parser = self._create_parser()

    @staticmethod
    def _create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Utility for managing RSA keys and encrypting .env file values.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""Examples:
  # Generate keys (if they don't exist)
  python encrypt_cli.py generate-keys

  # Encrypt values marked with '{ENCRYPTION_MARKER}' in config.env.template
  # using public_key.pem and write to .env
  python encrypt_cli.py encrypt -i config.env.template -o .env -k public_key.pem

  # Encrypt values and overwrite the input file, backing up the original
  python encrypt_cli.py encrypt -i config.env.template

  # Encrypt values and set a private key for decryption in config.env
  python encrypt_cli.py encrypt -i config.env.template --private-key keys/private_key.pem
""",
        )
        subparsers = parser.add_subparsers(
            dest="command", required=True, help="Available commands"
        )

        # --- Generate Keys Command ---
        parser_gen = subparsers.add_parser(
            "generate-keys", help="Generate RSA public and private keys."
        )
        parser_gen.add_argument(
            "--private-key",
            default=DEFAULT_PRIVATE_KEY_FILE,
            help=f"Path to save the private key (default: {DEFAULT_PRIVATE_KEY_FILE})",
        )
        parser_gen.add_argument(
            "--public-key",
            default=DEFAULT_PUBLIC_KEY_FILE,
            help=f"Path to save the public key (default: {DEFAULT_PUBLIC_KEY_FILE})",
        )
        parser_gen.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing key files without prompting.",
        )

        # --- Encrypt Command ---
        parser_enc = subparsers.add_parser(
            "encrypt",
            help=f"Encrypt marked values (ending with '{ENCRYPTION_MARKER}') in an .env file using a public key.",
        )
        parser_enc.add_argument(
            "-i",
            "--input",
            required=True,
            help="Path to the input .env file (e.g., config.env.template).",
        )
        parser_enc.add_argument(
            "-o",
            "--output",
            required=False,
            help="Path to write the output .env file with encrypted values (e.g., .env). "
            "If not provided, input file will be overwritten and original backed up.",
        )
        parser_enc.add_argument(
            "-k",
            "--public-key",
            default=DEFAULT_PUBLIC_KEY_FILE,
            help=f"Path to the public key PEM file (default: {DEFAULT_PUBLIC_KEY_FILE})",
        )
        parser_enc.add_argument(
            "--private-key",
            required=False,
            help="Path to the private key PEM file. If provided, updates the PRIVATE_KEY_PATH in the output file.",
        )
        return parser

    @staticmethod
    def _backup_input_file(input_path: Path):
        """Creates a backup of the input file with .original suffix."""
        original_backup = str(input_path) + ".original"

        # If .original already exists, find a unique name
        if Path(original_backup).exists():
            counter = 1
            while True:
                numbered_backup = f"{original_backup}.{counter}"
                if not Path(numbered_backup).exists():
                    original_backup = numbered_backup
                    break
                counter += 1

        # Create the backup
        logging.info(
            f"[EncryptCLI] Creating backup of {input_path} to {original_backup}"
        )
        shutil.copy2(input_path, original_backup)
        return Path(original_backup)

    @staticmethod
    def _update_private_key_path(env_file_path: Path, private_key_path: str):
        """Updates or adds the PRIVATE_KEY_PATH in the environment file."""
        logging.info(
            f"[EncryptCLI] Setting PRIVATE_KEY_PATH={private_key_path} in {env_file_path}"
        )

        # Read file content
        content_modified = False
        lines = []
        try:
            with open(env_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Look for existing PRIVATE_KEY_PATH line
            for i, line in enumerate(lines):
                if line.strip().startswith("PRIVATE_KEY_PATH="):
                    lines[i] = f"PRIVATE_KEY_PATH={private_key_path}\n"
                    content_modified = True
                    break

            # If PRIVATE_KEY_PATH not found, add it
            if not content_modified:
                lines.append(
                    f"\n# Path to private key for decryption\nPRIVATE_KEY_PATH={private_key_path}\n"
                )

            # Write back the updated content
            with open(env_file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            logging.info(f"[EncryptCLI] Updated PRIVATE_KEY_PATH in {env_file_path}")

        except Exception as e:
            logging.error(
                f"[EncryptCLI] Error updating PRIVATE_KEY_PATH in {env_file_path}: {e}"
            )
            raise

    def run(self):
        """Parses arguments and executes the corresponding command."""
        args = self.parser.parse_args()

        if args.command == "generate-keys":
            key_manager = KeyManager(args.private_key, args.public_key)
            key_manager.generate_and_save_keys(force_overwrite=args.force)

        elif args.command == "encrypt":
            key_manager = KeyManager(public_key_path=args.public_key)
            public_key = key_manager.load_public_key()
            encryptor = EncryptProcessor(public_key)
            processor = EnvFileProcessor(encryptor)

            input_path = Path(args.input)

            if args.output:
                # Normal operation with specified output
                output_path = Path(args.output)
                processor.process_file(str(input_path), str(output_path))

                # Update private key path if provided
                if args.private_key:
                    self._update_private_key_path(output_path, args.private_key)
            else:
                # No output provided - back up input file and overwrite it
                backup_path = self._backup_input_file(input_path)

                # Use input file as both source and destination
                processor.process_file(str(input_path), str(input_path))

                # Update private key path if provided
                if args.private_key:
                    self._update_private_key_path(input_path, args.private_key)

                logging.info(
                    f"[EncryptCLI] Input file {input_path} has been encrypted in-place"
                )
                logging.info(
                    f"[EncryptCLI] Original content backed up to {backup_path}"
                )


if __name__ == "__main__":
    cli = EncryptCLI()
    cli.run()
