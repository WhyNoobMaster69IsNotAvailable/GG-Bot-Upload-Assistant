#!/usr/bin/env python3

# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669

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
Config Documentation Generator

This script parses the configuration files in the samples directory and generates
markdown documentation based on the comments and structure.
"""

import os
import re
from pathlib import Path
import argparse
from typing import Dict, List


class ConfigDocGenerator:
    """Generates documentation from config files."""

    def __init__(self, input_path: str, output_path: str):
        """Initialize the config documentation generator.

        Args:
            input_path: Path to the config files or directory
            output_path: Path where documentation should be saved
        """
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def generate_docs(self):
        """Generate documentation for all config files."""
        if self.input_path.is_file():
            self._process_single_file(self.input_path)
        else:
            for root, dirs, files in os.walk(self.input_path):
                for file in files:
                    if file.endswith((".env", ".config.env")):
                        file_path = Path(root) / file
                        self._process_single_file(file_path)

    def _process_single_file(self, file_path: Path):
        """Process a single config file and generate documentation.

        Args:
            file_path: Path to the config file
        """
        print(f"Processing {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        sections = self._parse_sections(content)
        md_content = self._generate_markdown(file_path.name, sections)

        output_file = self.output_path / f"{file_path.stem.replace('.', '_')}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Documentation generated at {output_file}")

    def _parse_sections(self, content: str) -> List[Dict]:
        """Parse config file content into sections.

        Args:
            content: The content of the config file

        Returns:
            List of section dictionaries containing title and variables
        """
        # Split content by major section headers (those with #### format)
        # section_pattern = r"^#{3,}(.*?)#{3,}$"
        # section_blocks = re.split(section_pattern, content, flags=re.MULTILINE)

        # Process each section
        sections = []
        current_section = {"title": "General", "variables": []}

        lines = content.split("\n")
        current_comment = []

        for line in lines:
            # Check if this line is a section header
            if re.match(r"^#{3,}.*?#{3,}$", line):
                if current_section["variables"]:
                    sections.append(current_section)
                section_title = line.strip("#").strip()
                current_section = {"title": section_title, "variables": []}
                current_comment = []
                continue

            # Check if this line is a section header in another format
            if re.match(r"^#+\s*(.*?)\s*#+$", line):
                match = re.match(r"^#+\s*(.*?)\s*#+$", line)
                if match and match.group(1).strip():
                    if current_section["variables"]:
                        sections.append(current_section)
                    section_title = match.group(1).strip()
                    current_section = {"title": section_title, "variables": []}
                    current_comment = []
                    continue

            # Check if this is a comment line
            if line.strip().startswith("#"):
                comment_text = line.strip("# ")
                if comment_text:  # Skip empty comment lines
                    current_comment.append(comment_text)
            # Check if this is a variable definition
            elif "=" in line and not line.strip().startswith("#"):
                var_name, var_value = line.split("=", 1)
                var_name = var_name.strip()
                var_value = var_value.strip()

                if var_name:
                    current_section["variables"].append(
                        {
                            "name": var_name,
                            "value": var_value,
                            "description": "\n".join(current_comment),
                        }
                    )
                    current_comment = []

        # Add the last section
        if current_section["variables"]:
            sections.append(current_section)

        return sections

    def _generate_markdown(self, filename: str, sections: List[Dict]) -> str:
        """Generate markdown documentation from parsed sections.

        Args:
            filename: Name of the config file
            sections: List of section dictionaries

        Returns:
            Markdown formatted documentation
        """
        md = f"# {filename} Documentation\n\n"
        md += "<!-- Auto-generated documentation for configuration file -->\n\n"
        md += "## Table of Contents\n\n"

        # Generate TOC
        for section in sections:
            section_title = section["title"]
            section_anchor = section_title.lower().replace(" ", "-")
            md += f"- [{section_title}](#{section_anchor})\n"

        md += "\n"

        # Generate sections
        for section in sections:
            section_title = section["title"]
            md += f"## {section_title}\n\n"

            if section["variables"]:
                md += "| Variable | Default Value | Description |\n"
                md += "|----------|---------------|-------------|\n"

                for var in section["variables"]:
                    # Clean up the description for markdown table
                    description = var["description"].replace("\n", "<br>")
                    value = var["value"].replace("|", "\\|")

                    md += f"| `{var['name']}` | `{value}` | {description} |\n"

                md += "\n"

        return md


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate documentation from config files"
    )
    parser.add_argument(
        "--input",
        "-i",
        default="samples",
        help="Path to config files or directory (default: samples)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="docs/config",
        help="Output directory for documentation (default: docs/config)",
    )

    args = parser.parse_args()

    generator = ConfigDocGenerator(args.input, args.output)
    generator.generate_docs()

    print(f"Documentation generation complete. Files saved to {args.output}")


if __name__ == "__main__":
    main()
