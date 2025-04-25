#!/usr/bin/env python3

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

import sys
import re
from pathlib import Path

# The expected license header as a regular expression pattern
LICENSE_PATTERN = re.compile(
    r"""(?:^#!/usr/bin/env.*?\n\n)?"""
    r"""# GG Bot Upload Assistant\n"""
    r"""# Copyright \(C\) \d{4}(?:-\d{4})?  Noob Master669\n\n"""
    r"""# This program is free software: you can redistribute it and/or modify\n"""
    r"""# it under the terms of the GNU Affero General Public License as published\n"""
    r"""# by the Free Software Foundation, either version 3 of the License, or\n"""
    r"""# \(at your option\) any later version\.\n\n"""
    r"""# This program is distributed in the hope that it will be useful,\n"""
    r"""# but WITHOUT ANY WARRANTY; without even the implied warranty of\n"""
    r"""# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE\.  See the\n"""
    r"""# GNU Affero General Public License for more details\.\n\n"""
    r"""# You should have received a copy of the GNU Affero General Public License\n"""
    r"""# along with this program\.  If not, see <https://www\.gnu\.org/licenses/>\.\n""",
    re.MULTILINE,
)

# File extensions to check
EXTENSIONS_TO_CHECK = {".py"}

# Files and directories to exclude
EXCLUDED_PATHS = {
    "__pycache__",
    ".git",
    ".idea",
    "venv",
    ".venv",
    ".direnv",
    ".devenv",
    ".pytest_cache",
    ".ruff_cache",
}


def check_license_header(filename):
    """Check if the file has the required license header."""
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the file contains the license header
    return bool(LICENSE_PATTERN.search(content))


def main():
    """Main function to check license headers in files."""
    files_to_check = sys.argv[1:]
    files_missing_header = []

    for file_path in files_to_check:
        path = Path(file_path)

        # Skip excluded paths
        if any(excluded in path.parts for excluded in EXCLUDED_PATHS):
            continue

        # Only check files with specific extensions
        if path.suffix in EXTENSIONS_TO_CHECK and path.is_file():
            if not check_license_header(file_path):
                files_missing_header.append(file_path)

    if files_missing_header:
        print("The following files are missing the required license header:")
        for file in files_missing_header:
            print(f"  {file}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
