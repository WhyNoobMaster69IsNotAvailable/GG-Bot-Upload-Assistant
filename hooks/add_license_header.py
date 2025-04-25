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

import os
import sys
import re
from datetime import datetime
from pathlib import Path
import importlib.util

# Import check_license_header module from the same directory
script_dir = os.path.dirname(os.path.abspath(__file__))
check_license_header_path = os.path.join(script_dir, "check_license_header.py")
spec = importlib.util.spec_from_file_location("check_license_header", check_license_header_path)
check_license_header_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_license_header_module)

# Import required functions and variables from the module
check_license_header = check_license_header_module.check_license_header
EXTENSIONS_TO_CHECK = check_license_header_module.EXTENSIONS_TO_CHECK
EXCLUDED_PATHS = check_license_header_module.EXCLUDED_PATHS

# License header template with {year} placeholder
LICENSE_HEADER = """\
# GG Bot Upload Assistant
# Copyright (C) {year}  Noob Master669

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
"""


def add_license_header(file_path):
    """Add the license header to the file if it doesn't have one."""
    # Skip if file already has the header
    if check_license_header(file_path):
        return False  # No changes made

    # Get current year for the copyright notice
    current_year = datetime.now().year
    header = LICENSE_HEADER.format(year=current_year)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the file starts with a shebang
    shebang_match = re.match(r"^(#!/usr/bin/env.*?\n)", content)

    if shebang_match:
        # If there's a shebang, add header after it
        shebang = shebang_match.group(1)
        new_content = shebang + "\n" + header + "\n" + content[len(shebang) :].lstrip()
    else:
        # Otherwise, add header to the beginning
        new_content = header + "\n" + content

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True  # Changes made


def main():
    """Add license headers to all specified files or files in a directory."""
    if len(sys.argv) < 2:
        print(
            "Usage: add_license_header.py <file_or_directory> [file_or_directory ...]"
        )
        sys.exit(1)

    paths = sys.argv[1:]
    files_processed = 0
    files_modified = 0

    for path_str in paths:
        path = Path(path_str)

        if path.is_file():
            if path.suffix in EXTENSIONS_TO_CHECK:
                was_modified = add_license_header(str(path))
                files_processed += 1
                if was_modified:
                    files_modified += 1
                    print(f"Added license header to {path}")
        elif path.is_dir():
            for root, dirs, files in os.walk(path):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if d not in EXCLUDED_PATHS]

                for file in files:
                    file_path = os.path.join(root, file)
                    if Path(file_path).suffix in EXTENSIONS_TO_CHECK:
                        was_modified = add_license_header(file_path)
                        files_processed += 1
                        if was_modified:
                            files_modified += 1
                            print(f"Added license header to {file_path}")

    if files_modified > 0:
        print(f"Added license headers to {files_modified} out of {files_processed} files processed")
    
    # Always exit with 0 to satisfy pre-commit "fixing" behavior
    sys.exit(0)


if __name__ == "__main__":
    main()
