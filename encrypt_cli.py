import argparse
import logging

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
            required=True,
            help="Path to write the output .env file with encrypted values (e.g., .env).",
        )
        parser_enc.add_argument(
            "-k",
            "--public-key",
            default=DEFAULT_PUBLIC_KEY_FILE,
            help=f"Path to the public key PEM file (default: {DEFAULT_PUBLIC_KEY_FILE})",
        )
        return parser

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
            processor.process_file(args.input, args.output)


if __name__ == "__main__":
    cli = EncryptCLI()
    cli.run()
