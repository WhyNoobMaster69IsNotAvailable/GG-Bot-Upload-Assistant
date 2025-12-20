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
HTML Documentation Generator for Config Files

This script generates interactive HTML documentation from environment config files.
"""

import os
import re
from pathlib import Path
import argparse
from typing import Dict, List, Any
import html


class HtmlDocGenerator:
    """Generates interactive HTML documentation from config files."""

    def __init__(self, input_path: str, output_path: str):
        """Initialize the HTML documentation generator.

        Args:
            input_path: Path to the config files or directory
            output_path: Path where HTML files should be saved
        """
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def generate_docs(self):
        """Generate HTML documentation for all config files."""
        # Create index file first
        self._create_index()

        # Process individual files
        if self.input_path.is_file():
            self._process_single_file(self.input_path)
        else:
            for root, dirs, files in os.walk(self.input_path):
                for file in files:
                    if file.endswith((".env", ".config.env")):
                        file_path = Path(root) / file
                        self._process_single_file(file_path)

    def _create_index(self):
        """Create index.html file with links to all documentation pages."""
        index_content = self._get_html_template("Config Files Documentation", "index")

        # Will be populated with links to individual doc pages
        file_links = []

        if self.input_path.is_file():
            # Single file mode
            file_links.append(
                f'<li><a href="{self.input_path.stem.replace(".", "_")}.html">{self.input_path.name}</a></li>'
            )
        else:
            # Directory mode - scan for files
            config_files = []
            for root, dirs, files in os.walk(self.input_path):
                for file in files:
                    if file.endswith((".env", ".config.env")):
                        rel_path = os.path.relpath(
                            os.path.join(root, file), self.input_path
                        )
                        file_path = Path(rel_path)
                        config_files.append(
                            (file_path.name, file_path.stem.replace(".", "_") + ".html")
                        )

            # Sort the files alphabetically
            config_files.sort()

            for file_name, html_file in config_files:
                file_links.append(f'<li><a href="{html_file}">{file_name}</a></li>')

        # Complete the index page with the file list
        index_content = index_content.replace(
            "{{CONTENT}}",
            f"""
            <h1>Config Files Documentation</h1>
            <p>This documentation is automatically generated from the configuration files.</p>
            <h2>Available Configuration Files</h2>
            <ul>
                {"".join(file_links)}
            </ul>
        """,
        )

        # Write index file
        with open(self.output_path / "index.html", "w", encoding="utf-8") as f:
            f.write(index_content)

        # Copy CSS and JS
        self._write_css_file()
        self._write_js_file()

    def _process_single_file(self, file_path: Path):
        """Process a single config file and generate HTML documentation.

        Args:
            file_path: Path to the config file
        """
        print(f"Processing {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse content into sections
        sections = self._parse_sections(content)

        # Generate HTML content
        html_content = self._generate_html(file_path.name, sections)

        # Write the output file
        output_file = self.output_path / f"{file_path.stem.replace('.', '_')}.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"HTML documentation generated at {output_file}")

    def _parse_sections(self, content: str) -> List[Dict[str, Any]]:
        """Parse config file content into sections.

        Args:
            content: The content of the config file

        Returns:
            List of section dictionaries
        """
        sections = []
        lines = content.split("\n")

        current_section = {"title": "General", "description": "", "variables": []}
        current_comment = []
        in_section_description = False

        for line in lines:
            # Check for section headers
            section_header_match = re.match(r"^#{3,}\s*(.*?)\s*#{3,}$", line)
            if section_header_match or re.match(r"^#{1,}\s*(.*?)\s*#{1,}$", line):
                # Save the previous section if it has variables
                if current_section["variables"]:
                    sections.append(current_section)

                # Extract the title
                if section_header_match:
                    section_title = section_header_match.group(1).strip()
                else:
                    match = re.match(r"^#{1,}\s*(.*?)\s*#{1,}$", line)
                    section_title = match.group(1).strip() if match else "General"

                # Create a new section
                current_section = {
                    "title": section_title,
                    "description": "",
                    "variables": [],
                }
                current_comment = []
                in_section_description = (
                    True  # Next comments are for section description
                )
                continue

            # Collect comments
            if line.strip().startswith("#"):
                comment_text = line.strip("# ")
                if comment_text:  # Skip empty comment lines
                    if in_section_description:
                        # Add to section description
                        if current_section["description"]:
                            current_section["description"] += "\n" + comment_text
                        else:
                            current_section["description"] = comment_text
                    else:
                        # Add to current variable comment
                        current_comment.append(comment_text)

            # Process variable definitions
            elif "=" in line and not line.strip().startswith("#"):
                in_section_description = False  # No longer in section description

                var_name, var_value = line.split("=", 1)
                var_name = var_name.strip()
                var_value = var_value.strip()

                if var_name:
                    var_type = self._infer_type(var_value)
                    is_required = var_value != "" and not var_name.startswith("#")

                    current_section["variables"].append(
                        {
                            "name": var_name,
                            "value": var_value,
                            "description": "\n".join(current_comment),
                            "type": var_type,
                            "required": is_required,
                        }
                    )
                    current_comment = []

        # Add the last section
        if current_section["variables"]:
            sections.append(current_section)

        return sections

    def _infer_type(self, value: str) -> str:
        """Infer the type of a variable based on its value.

        Args:
            value: The variable's value as a string

        Returns:
            The inferred type as a string
        """
        if value.lower() in ("true", "false"):
            return "boolean"

        try:
            int(value)
            return "integer"
        except ValueError:
            try:
                float(value)
                return "number"
            except ValueError:
                pass

        # Check for arrays
        if "," in value and not value.startswith('"') and not value.startswith("'"):
            return "array"

        return "string"

    def _generate_html(self, filename: str, sections: List[Dict[str, Any]]) -> str:
        """Generate HTML documentation from parsed sections.

        Args:
            filename: Name of the config file
            sections: List of section dictionaries

        Returns:
            HTML documentation
        """
        # Get the base template
        html_content = self._get_html_template(f"{filename} Documentation", filename)

        # Generate table of contents
        toc = "<ul class='toc'>"
        for section in sections:
            section_id = self._make_id(section["title"])
            toc += f"<li><a href='#{section_id}'>{section['title']}</a></li>"
        toc += "</ul>"

        # Generate sections content
        sections_html = ""
        for section in sections:
            section_id = self._make_id(section["title"])

            # Start section
            sections_html += f"""
            <div class='config-section' id='{section_id}'>
                <h2>{section['title']}</h2>
                <div class='section-description'>{self._format_description(section['description'])}</div>
            """

            # Add variables table
            if section["variables"]:
                sections_html += """
                <table class='variables-table'>
                    <thead>
                        <tr>
                            <th>Variable</th>
                            <th>Type</th>
                            <th>Default</th>
                            <th>Required</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                """

                for var in section["variables"]:
                    var_name = html.escape(var["name"])
                    var_type = html.escape(var["type"])
                    var_value = html.escape(var["value"] or "''")
                    var_required = "Yes" if var["required"] else "No"
                    var_description = self._format_description(var["description"])

                    sections_html += f"""
                    <tr class='variable-row' data-name='{var_name}'>
                        <td class='var-name'><code>{var_name}</code></td>
                        <td class='var-type'><span class='type-badge type-{var_type}'>{var_type}</span></td>
                        <td class='var-default'><code>{var_value}</code></td>
                        <td class='var-required'>{var_required}</td>
                        <td class='var-description'>{var_description}</td>
                    </tr>
                    """

                sections_html += """
                    </tbody>
                </table>
                """

            # End section
            sections_html += "</div>"

        # Assemble the final content
        main_content = f"""
        <h1>{filename} Documentation</h1>
        <div class='description'>
            <p>This documentation is automatically generated from the configuration file.</p>
            <a href='index.html' class='back-link'>Back to Index</a>
        </div>

        <h2>Table of Contents</h2>
        {toc}

        <div class='filter-container'>
            <input type='text' id='variable-filter' placeholder='Filter variables...' class='filter-input'>
            <div class='filter-options'>
                <label><input type='checkbox' id='show-required-only'> Show required only</label>
            </div>
        </div>

        <div class='sections-container'>
            {sections_html}
        </div>
        """

        # Replace the content placeholder
        html_content = html_content.replace("{{CONTENT}}", main_content)

        return html_content

    def _format_description(self, description: str) -> str:
        """Format a description string as HTML.

        Args:
            description: Raw description text

        Returns:
            HTML formatted description
        """
        if not description:
            return ""

        # Escape HTML special characters
        description = html.escape(description)

        # Convert newlines to <br> tags
        description = description.replace("\n", "<br>")

        # Make URLs clickable
        url_pattern = r'https?://[^\s<>"]+'
        description = re.sub(
            url_pattern, r'<a href="\g<0>" target="_blank">\g<0></a>', description
        )

        return description

    def _make_id(self, text: str) -> str:
        """Convert a string to a valid HTML ID.

        Args:
            text: Input text

        Returns:
            Valid HTML ID
        """
        # Remove special characters
        id_text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        # Replace spaces with hyphens
        id_text = re.sub(r"\s+", "-", id_text).lower()
        return id_text

    def _get_html_template(self, title: str, page_id: str) -> str:
        """Get the HTML template for documentation pages.

        Args:
            title: Page title
            page_id: Unique page identifier

        Returns:
            HTML template
        """
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body data-page-id="{page_id}">
    <div class="container">
        {{{{CONTENT}}}}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    def _write_css_file(self):
        """Write the CSS file for styling the documentation."""
        css_content = """
:root {
    --primary-color: #3498db;
    --secondary-color: #2980b9;
    --text-color: #333;
    --light-bg: #f8f9fa;
    --border-color: #ddd;
    --header-bg: #2c3e50;
    --header-text: #ecf0f1;
    --type-string: #2ecc71;
    --type-number: #3498db;
    --type-boolean: #9b59b6;
    --type-array: #e67e22;
    --type-object: #34495e;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    background-color: white;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    min-height: 100vh;
}

h1 {
    color: var(--header-bg);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary-color);
}

h2 {
    color: var(--header-bg);
    margin-top: 2rem;
    margin-bottom: 1rem;
}

p {
    margin-bottom: 1rem;
}

a {
    color: var(--primary-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.toc {
    background-color: var(--light-bg);
    padding: 1rem;
    border-radius: 5px;
    margin-bottom: 2rem;
    list-style-type: none;
}

.toc li {
    margin-bottom: 0.5rem;
}

.toc a {
    display: block;
    padding: 0.25rem 0;
}

.config-section {
    margin-bottom: 3rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.section-description {
    margin-bottom: 1rem;
}

.variables-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 2rem;
}

.variables-table th,
.variables-table td {
    text-align: left;
    padding: 0.75rem;
    border-bottom: 1px solid var(--border-color);
}

.variables-table th {
    background-color: var(--light-bg);
    font-weight: 600;
}

.variables-table tr:hover {
    background-color: rgba(0, 0, 0, 0.02);
}

.variables-table code {
    background-color: var(--light-bg);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.9rem;
    max-width: 300px;
    overflow-x: auto;
    display: inline-block;
    word-break: break-all;
}

.type-badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 3px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    color: white;
}

.type-string {
    background-color: var(--type-string);
}

.type-integer, .type-number {
    background-color: var(--type-number);
}

.type-boolean {
    background-color: var(--type-boolean);
}

.type-array {
    background-color: var(--type-array);
}

.type-object {
    background-color: var(--type-object);
}

.var-name {
    width: 20%;
}

.var-type {
    width: 10%;
}

.var-default {
    width: 15%;
}

.var-required {
    width: 10%;
    text-align: center;
}

.var-description {
    width: 45%;
}

.filter-container {
    margin-bottom: 2rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 1rem;
}

.filter-input {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    border-radius: 3px;
    font-size: 1rem;
    flex-grow: 1;
    min-width: 250px;
}

.filter-options {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.filter-options label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.back-link {
    display: inline-block;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
    padding: 0.5rem 1rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: 3px;
    text-decoration: none;
}

.back-link:hover {
    background-color: var(--secondary-color);
    text-decoration: none;
}

@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }

    .variables-table {
        display: block;
        overflow-x: auto;
    }

    .var-name, .var-type, .var-default, .var-required, .var-description {
        width: auto;
    }
}
        """

        with open(self.output_path / "style.css", "w", encoding="utf-8") as f:
            f.write(css_content)

    def _write_js_file(self):
        """Write the JavaScript file for interactive features."""
        js_content = """
document.addEventListener('DOMContentLoaded', function() {
    const variableFilter = document.getElementById('variable-filter');
    const showRequiredOnly = document.getElementById('show-required-only');

    if (!variableFilter || !showRequiredOnly) return;

    // Filter variables based on search and filters
    function filterVariables() {
        const searchTerm = variableFilter.value.toLowerCase();
        const requiredOnly = showRequiredOnly.checked;

        document.querySelectorAll('.variable-row').forEach(row => {
            const varName = row.querySelector('.var-name').textContent.toLowerCase();
            const varDescription = row.querySelector('.var-description').textContent.toLowerCase();
            const isRequired = row.querySelector('.var-required').textContent === 'Yes';

            const matchesSearch = searchTerm === '' ||
                varName.includes(searchTerm) ||
                varDescription.includes(searchTerm);

            const matchesFilter = !requiredOnly || isRequired;

            row.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
        });

        // Hide sections that have no visible variables
        document.querySelectorAll('.config-section').forEach(section => {
            const visibleRows = Array.from(section.querySelectorAll('.variable-row'))
                .filter(row => row.style.display !== 'none');

            section.style.display = visibleRows.length > 0 ? '' : 'none';
        });
    }

    // Event listeners
    variableFilter.addEventListener('input', filterVariables);
    showRequiredOnly.addEventListener('change', filterVariables);

    // Initialize smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        });
    });
});
        """

        with open(self.output_path / "script.js", "w", encoding="utf-8") as f:
            f.write(js_content)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate HTML documentation from config files"
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
        default="docs/html",
        help="Output directory for HTML files (default: docs/html)",
    )

    args = parser.parse_args()

    generator = HtmlDocGenerator(args.input, args.output)
    generator.generate_docs()

    print(f"HTML documentation generation complete. Files saved to {args.output}")


if __name__ == "__main__":
    main()
