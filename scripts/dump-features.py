#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2008-2016 Canonical, Ltd.
# Author: Kees Cook <kees@ubuntu.com>
# Copyright 2025 Canonical, Ltd.
# Author: Marek Suchánek <marek.suchanek@canonical.com>
# Author: John Breton <john.breton@canonical.com>
# License: GPLv3

import argparse
import json
import logging
import sys
from enum import Enum, auto
from io import TextIOWrapper
from typing import Dict, List, Optional, Tuple

try:
    from pydantic import BaseModel, Field, ValidationError
except ModuleNotFoundError:
    print("Please install the Pydantic Python library.", file=sys.stderr)
    print("On Ubuntu and Debian:", file=sys.stderr)
    print("$ sudo apt install python3-pydantic", file=sys.stderr)
    sys.exit(1)


# --- Constants ---
PROGRAM_NAME = 'dump-features'
PROGRAM_DESCRIPTION = '''
This program generates a table with ReStructuredText markup that lists
Ubuntu security features and their status in various Ubuntu releases.
'''

# --- Logging Setup ---
def setup_logging():
    """Configure logging to output errors to stderr."""
    logger = logging.getLogger(PROGRAM_NAME)
    logger.setLevel(logging.ERROR)

    # Create handler that writes to stderr
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.ERROR)

    # Create formatter
    formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


# Initialize logger
logger = setup_logging()


# --- Data Models ---
class State(Enum):
    """Possible states for a security feature implementation."""
    UNIMPLEMENTED = "UNIMPLEMENTED"
    AVAILABLE = "AVAILABLE"
    DEFAULT = "DEFAULT"


class Release(BaseModel):
    """Represents an Ubuntu release as described in releases.json."""
    code_name: str
    human_name: str
    is_eol: bool

    def get_version_only(self) -> str:
        """
        Prettify a release by removing "Ubuntu".

        Example: "Ubuntu 24.04 LTS" -> "24.04 LTS"
        """
        return self.human_name.replace("Ubuntu ", "")

    def is_esm(self) -> bool:
        """Check if this is an ESM release."""
        return '/esm' in self.code_name or 'ESM' in self.human_name


class Implementation(BaseModel):
    """
    Represents the implementation status of a security feature
    in a given Ubuntu release.
    """
    comment: str
    state: State

    @classmethod
    def create_initial(cls) -> 'Implementation':
        """Create an initial unimplemented state."""
        return cls(comment="--", state=State.UNIMPLEMENTED)


class Feature(BaseModel):
    """Represents a security feature as listed in features.json."""
    name: str
    section: bool = Field(default=False)
    changes: Dict[str, Implementation] = Field(default_factory=dict)


# --- Command Line Interface ---
def parse_arguments() -> argparse.Namespace:
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION
    )

    parser.add_argument(
        '-H', '--historical',
        help='Display all releases, including EOL',
        action='store_true'
    )
    parser.add_argument(
        '-o', '--output',
        help='Write the table to the specified file; otherwise, print to stdout',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout
    )
    parser.add_argument(
        '-r', '--releases',
        help='Read release data from this file; by default "./releases.json"',
        nargs='?',
        type=argparse.FileType('r'),
        default='releases.json'
    )
    parser.add_argument(
        '-f', '--features',
        help='Read feature data from this file; by default "./features.json"',
        nargs='?',
        type=argparse.FileType('r'),
        default='features.json'
    )
    parser.add_argument(
        '-t', '--tabs',
        help='Generate output with tabs (requires sphinx-tabs or sphinx-design)',
        action='store_true'
    )
    parser.add_argument(
        '--tab-extension',
        help='Tab extension to use: "sphinx-tabs" or "sphinx-design" (default: sphinx-tabs)',
        choices=['sphinx-tabs', 'sphinx-design'],
        default='sphinx-tabs'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Enable verbose logging (INFO level)',
        action='store_true'
    )
    parser.add_argument(
        '-d', '--debug',
        help='Enable debug logging (DEBUG level)',
        action='store_true'
    )
    return parser.parse_args()


# --- Data Loading Functions ---
def load_releases(file: TextIOWrapper) -> List[Release]:
    """Load and validate releases from a JSON file."""
    try:
        logger.debug(f"Loading releases from {file.name}")
        raw_releases = json.load(file)
        releases =  [Release(**r) for r in raw_releases]
        logger.info(f"Successfully loaded {len(releases)} releases")
        return releases
    except ValidationError as e:
        logger.error(f"Error validating releases: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing releases JSON: {e}")
        sys.exit(1)


def load_features(file: TextIOWrapper) -> Tuple[List[Feature], Dict]:
    """Load and validate features from a JSON file."""
    try:
        logger.debug(f"Loading features from {file.name}")
        raw_features = json.load(file)
        feature_to_section = build_section_mapping(raw_features)
        features = [Feature(**f) for f in raw_features]
        logger.info(f"Successfully loaded {len(features)} features")
        return features, feature_to_section
    except ValidationError as e:
        logger.error(f"Error validating features: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing features JSON: {e}")
        sys.exit(1)


def build_section_mapping(raw_features: List[dict]) -> Dict:
    """
    Build a mapping from feature names to their section information.

    Args:
        raw_features: A List of raw feature dictionaries from JSON

    Returns:
        A dictionary mapping feature names to section information
    """
    feature_to_section = {}
    current_section_name = None

    for feature_dict in raw_features:
        if feature_dict.get("section"):
            current_section_name = feature_dict["name"]
            logger.debug(f"Found section: {current_section_name}")
        elif "name" in feature_dict and current_section_name:
            feature_to_section[feature_dict["name"]] = {
                "name": current_section_name,
            }

    logger.debug(f"Built section mapping for {len(feature_to_section)} features")
    return feature_to_section


# --- Table Generation Functions ---
class TableGenerator:
    """Handles RST table generation for security features."""

    def __init__(self, output_file: TextIOWrapper, show_historical: bool, use_tabs: bool = False, tab_extension: str = 'sphinx-tabs'):
        self.output = output_file
        self.show_historical = show_historical
        self.use_tabs = use_tabs
        self.tab_extension = tab_extension

    def format_table_row(self, cells: List[str]) -> str:
        """
        Format a list of cells as an RST list table row.

        Args:
            cells: A List of cell contents

        Returns:
            A formatted RST table row string
        """
        if not cells:
            return ""

        row_lines = []
        for i, cell in enumerate(cells):
            if i == 0:
                row_lines.append(f"   * - {cell}")
            else:
                row_lines.append(f"     - {cell}")

        return '\n'.join(row_lines) + '\n'

    def write_page(self, releases: List[Release], features: List[Feature], feature_to_section: Dict):
        """Write the page with optional tabs."""
        if self.use_tabs:
            logger.debug("Using tabbed output format")
            self._write_tabbed_content(releases, features, feature_to_section)
        else:
            logger.debug("Using single table output format")
            self._write_single_table(releases, features, feature_to_section)

    def _write_tabbed_content(self, releases: List[Release], features: List[Feature], feature_to_section: Dict):
        """Write content with tabs for different release types."""
        # Separate releases into categories
        esm_releases = [r for r in releases if r.is_esm() and not r.is_eol]
        current_releases = [r for r in releases if not r.is_esm() and not r.is_eol]

        logger.debug(f"Split releases: {len(current_releases)} current, {len(esm_releases)} ESM")

        # Start tabs based on extension type
        if self.tab_extension == 'sphinx-tabs':
            self._write_sphinx_tabs(esm_releases, current_releases, features, feature_to_section)
        else:
            self._write_sphinx_design_tabs(esm_releases, current_releases, features, feature_to_section)

    def _write_sphinx_tabs(self, esm_releases: List[Release], current_releases: List[Release], features: List[Feature], feature_to_section: Dict):
        """Write tabs using sphinx-tabs extension."""
        self.output.write(".. tabs::\n\n")

        # Current releases tab
        self.output.write("   .. tab:: Current Releases\n\n")
        self.output.write("      **Supported LTS and Interim Releases**\n\n")
        self._write_table_for_releases(current_releases, features, feature_to_section, indent=6)

        # ESM releases tab
        if esm_releases:
            self.output.write("\n   .. tab:: ESM Releases\n\n")
            self.output.write("      **Extended Security Maintenance Releases**\n\n")
            self._write_table_for_releases(esm_releases, features, feature_to_section, indent=6)

    def _write_sphinx_design_tabs(self, esm_releases: List[Release], current_releases: List[Release], features: List[Feature], feature_to_section: Dict):
        """Write tabs using sphinx-design extension."""
        self.output.write(".. tab-set::\n\n")

        # Current releases tab
        self.output.write("   .. tab-item:: Current Releases\n")
        self.output.write("      :sync: current\n\n")
        self.output.write("      **Supported LTS and Interim Releases**\n\n")
        self._write_table_for_releases(current_releases, features, feature_to_section, indent=6)

        # ESM releases tab
        if esm_releases:
            self.output.write("\n   .. tab-item:: ESM Releases\n")
            self.output.write("      :sync: esm\n\n")
            self.output.write("      **Extended Security Maintenance Releases**\n\n")
            self._write_table_for_releases(esm_releases, features, feature_to_section, indent=6)

    def _write_table_for_releases(self, releases: List[Release], features: List[Feature], feature_to_section: Dict, indent: int = 0):
        """Write a table for a specific set of releases."""
        indent_str = ' ' * indent

        # Start the table
        self.output.write(f"{indent_str}.. list-table:: Security features\n")
        self.output.write(f"{indent_str}   :header-rows: 1\n\n")

        # Create header row
        release_names = [r.get_version_only() for r in releases]
        header_cells = ["Section", "Feature"] + release_names

        # Write header with proper indentation
        header_row = self.format_table_row(header_cells)
        indented_header = '\n'.join(indent_str + line if line else '' for line in header_row.split('\n'))
        self.output.write(indented_header)

        # Write feature rows
        feature_count = 1
        for feature in features:
            if not feature.section:
                cells = self._build_feature_row_cells(feature, releases, feature_to_section)
                row = self.format_table_row(cells)
                indented_row = '\n'.join(indent_str + line if line else '' for line in row.split('\n'))
                self.output.write(indented_row)
                feature_count += 1

        logger.debug(f"Wrote {feature_count} feature rows for {len(releases)} releases")

    def _write_single_table(self, releases: List[Release], features: List[Feature], feature_to_section: Dict):
        """Write a single table without tabs (original behavior)."""

        self.output.write(".. list-table:: Security features in releases\n")
        self.output.write("   :header-rows: 1\n\n")

        # Filter releases based on the historical flag
        header_releases = self._get_display_releases(releases)

        # Create the header row
        release_names = [r.get_version_only() for r in header_releases]
        header_cells = ["Section", "Feature"] + release_names

        self.output.write(self.format_table_row(header_cells))
        self.output.write("\n")

        # Write feature rows
        feature_count = 0
        for feature in features:
            if not feature.section:
                cells = self._build_feature_row_cells(feature, header_releases, feature_to_section)
                self.output.write(self.format_table_row(cells))
                self.output.write('\n')
                feature_count += 1

        logger.debug(f"Wrote {feature_count} feature rows for {len(header_releases)} releases")

    def _get_display_releases(self, releases: List[Release]) -> List[Release]:
        """Get the list of releases to display based on historical flag."""
        if self.show_historical:
            return releases
        return [r for r in releases if not r.is_eol]

    def _build_feature_row_cells(self, feature: Feature, releases: List[Release], feature_to_section: Dict) -> List[str]:
        """Build the cell contents for a feature row."""
        cells = []

        # Add the section reference
        section_info = feature_to_section.get(feature.name, {})
        section_cell = f":ref:`{section_info['name']}`" if section_info else ""
        cells.append(section_cell)

        # Add the feature reference
        cells.append(f":ref:`{feature.name}`")

        # Add the implementation status for each release
        for release in releases:
            # Create a clean code name without modifying the original release object
            if release.code_name.endswith("/esm"):
                clean_code_name = release.code_name[:-4]  # Remove the last 4 characters "/esm"
            else:
                clean_code_name = release.code_name

            # Only show value if there's an explicit entry, otherwise show "--"
            if clean_code_name in feature.changes:
                implementation = feature.changes[clean_code_name]
                cells.append(implementation.comment)
            else:
                cells.append("--")

        return cells

# --- Script Entry Point ---
def main():
    """Main program entry point."""
    # Parse the command line arguments
    args = parse_arguments()

    # Configure logging based on command line arguments
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.handlers[0].setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    elif args.verbose:
        logger.setLevel(logging.INFO)
        logger.handlers[0].setLevel(logging.INFO)
        logger.info("Verbose logging enabled")

    # Load data
    releases = load_releases(args.releases)
    features, feature_to_section = load_features(args.features)

    # Create table generator
    generator = TableGenerator(args.output, args.historical, args.tabs, args.tab_extension)

    # Generate the output
    generator.write_page(releases, features, feature_to_section)

    # Ensure the output is written
    args.output.flush()


if __name__ == "__main__":
    main()
