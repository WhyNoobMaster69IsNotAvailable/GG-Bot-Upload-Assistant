# License Header Tools

This repository includes tools to ensure all Python files have the required license header.

## Pre-commit Hook

A pre-commit hook has been set up to automatically add the required AGPL license header to any Python files being committed that don't already have it. This means you never have to worry about manually adding the license header to your files.

### Setup

1. Make sure pre-commit is installed:
   ```
   pip install pre-commit
   ```

2. Install the pre-commit hooks:
   ```
   pre-commit install
   ```

## License Header Format

The automatically added license header format is:

```python
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
```

The `{year}` will be automatically replaced with the current year.

## Manually Adding License Headers

If you want to manually add the license header to files without committing them, you can use the `hooks/add_license_header.py` script:

```
./hooks/add_license_header.py <file_or_directory> [file_or_directory ...]
```

### Examples:

Add license header to a single file:
```
./hooks/add_license_header.py path/to/file.py
```

Add license headers to all Python files in a directory:
```
./hooks/add_license_header.py path/to/directory/
```

Add license headers to all Python files in multiple directories:
```
./hooks/add_license_header.py directory1/ directory2/ file3.py
```

## Checking License Headers

To check if files have the license header without attempting to add it:

```
./hooks/check_license_header.py <file1> [file2 ...]
```

This will print a list of files that are missing the license header and exit with code 1 if any are found. 