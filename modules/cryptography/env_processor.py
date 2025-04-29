import logging
import sys
from pathlib import Path
from typing import Optional, List

from modules.cryptography import ENCRYPTION_MARKER
from modules.cryptography.encrypt_decrypt_processor import EncryptProcessor


class EnvFileProcessor:
    """Reads/writes .env files and encrypts marked values."""

    def __init__(self, value_encryptor: EncryptProcessor):
        self.encryptor = value_encryptor

    def process_file(self, input_env_path: str, output_env_path: str):
        """Reads input .env, encrypts marked values, and writes to output .env."""
        logging.info(f"[EnvFileProcessor] Processing input file: {input_env_path}")

        input_path = Path(input_env_path)
        if not input_path.is_file():
            logging.error(f"[EnvFileProcessor] Input file not found: {input_env_path}")
            sys.exit(1)

        output_path = Path(output_env_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = self._read_input_file(input_path)
        if lines is None:
            sys.exit(1)  # Error already logged

        self._write_output_file(output_path, lines)

    @staticmethod
    def _read_input_file(input_path: Path) -> Optional[List[str]]:
        """Reads lines from the input file."""
        try:
            with open(input_path, "r", encoding="utf-8") as infile:
                return infile.readlines()
        except Exception as e:
            logging.error(f"Error reading input file {input_path}: {e}")
            return None

    def _write_output_file(self, output_path: Path, lines: List[str]):
        """Writes processed lines to the output file."""
        num_encrypted = 0
        num_skipped_length = 0
        num_skipped_empty = 0

        try:
            with open(output_path, "w", encoding="utf-8") as outfile:
                for i, line in enumerate(lines, 1):
                    stripped_line = line.strip()
                    should_process = False  # Flag to indicate if line is a candidate

                    # Check if line is potentially marked for encryption
                    if (
                        stripped_line.endswith(ENCRYPTION_MARKER)
                        and "=" in stripped_line
                    ):
                        # Try processing it
                        line_without_marker = stripped_line[
                            : stripped_line.rfind(ENCRYPTION_MARKER)
                        ].strip()
                        parts = line_without_marker.split("=", 1)

                        # Check for valid KEY=VALUE format
                        if len(parts) == 2:
                            key, value_to_encrypt = parts[0].strip(), parts[1].strip()

                            # Check for valid key format
                            if key and " " not in key and not key.startswith("#"):
                                # It looks like a valid candidate for encryption
                                should_process = True
                            else:  # Invalid key format
                                logging.warning(
                                    f"[EnvFileProcessor] Line {i}: Invalid key format '{key}'. Writing original line (marker preserved)."
                                )
                        else:  # Invalid KEY=VALUE format
                            logging.warning(
                                f"[EnvFileProcessor] Line {i}: Marker found but not a valid KEY=VALUE format. Writing original line (marker preserved)."
                            )

                    # Process the line only if it passed initial validation
                    if should_process:
                        # Key and value_to_encrypt are already defined from checks above
                        # Remove quotes
                        if (
                            len(value_to_encrypt) >= 2
                            and value_to_encrypt.startswith(("'", '"'))
                            and value_to_encrypt.endswith(value_to_encrypt[0])
                        ):
                            value_to_encrypt = value_to_encrypt[1:-1]

                        # Handle empty value after unquoting
                        if not value_to_encrypt:
                            logging.info(
                                f"[EnvFileProcessor] Line {i}: Writing empty value for key '{key}' (marker removed)."
                            )
                            outfile.write(f"{key}=\n")
                            num_skipped_empty += 1
                            continue  # Processed, move to next line

                        # Attempt encryption
                        logging.info(
                            f"[EnvFileProcessor] Line {i}: Attempting to encrypt value for key '{key}'"
                        )
                        encrypted_value = self.encryptor.encrypt(value_to_encrypt)

                        if encrypted_value is None:
                            # Encryption skipped or failed
                            logging.warning(
                                f"[EnvFileProcessor] Line {i}: Encryption skipped or failed for key '{key}'. Writing original value (marker removed)."
                            )
                            outfile.write(
                                line_without_marker + "\n"
                            )  # Write original line without marker
                            num_skipped_length += 1
                            continue  # Processed, move to next line
                        else:
                            # Encryption succeeded
                            outfile.write(f"{key}=ENC::{encrypted_value}\n")
                            num_encrypted += 1
                            continue  # Processed, move to next line

                    # Default: Write the original line if not processed above or if processing failed validation checks
                    outfile.write(line)

        except Exception as e:
            logging.error(
                f"[EnvFileProcessor] Error writing to output file {output_path}: {e}"
            )
            sys.exit(1)

        logging.info(
            f"[EnvFileProcessor] Processing complete. Output written to {output_path}"
        )
        logging.info(
            f"[EnvFileProcessor]   - Values successfully encrypted: {num_encrypted}"
        )
        logging.info(
            f"[EnvFileProcessor]   - Values skipped (empty):      {num_skipped_empty}"
        )
        logging.info(
            f"[EnvFileProcessor]   - Values skipped (too long/error): {num_skipped_length}"
        )
