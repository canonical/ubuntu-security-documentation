#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2025 Canonical, Ltd.
# Author: John Breton <john.breton@canonical.com>
# License: GPLv3

import argparse
import json
import re
import sys
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("Please install required Python libraries.", file=sys.stderr)
    print("On Ubuntu and Debian:", file=sys.stderr)
    print("$ sudo apt install python3-requests python3-bs4", file=sys.stderr)
    sys.exit(1)


# --- Constants ---
PROGRAM_NAME = 'update-features'
PROGRAM_DESCRIPTION = '''
This program scrapes the Ubuntu Security Features wiki page and updates
the features.json file with any new or changed data.
'''

# Source of truth, needs to be updated if features find a new home
WIKI_URL = 'https://wiki.ubuntu.com/Security/Features'

# Mapping of states based on background colors from the wiki
#
# Yeah don't worry I think this is dumb too
STATE_COLOR_MAP = {
    '#00dd00': 'DEFAULT',      # Green - Default/enabled
    '#98fd98': 'AVAILABLE',    # Light green - Available
    '#dddddd': 'UNIMPLEMENTED' # Gray - Unimplemented
}


# --- Utility Functions ---
def print_error(*args, **kwargs):
    """Print message to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def print_info(*args, **kwargs):
    """Print informational message."""
    print(*args, **kwargs)


# --- Command Line Interface ---
def parse_arguments() -> argparse.Namespace:
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION
    )

    parser.add_argument(
        '-f', '--features',
        help='Path to features.json file to update; by default "./features.json"',
        nargs='?',
        type=str,
        default='features.json'
    )
    parser.add_argument(
        '-r', '--releases',
        help='Path to releases.json file for version mapping; by default "./releases.json"',
        nargs='?',
        type=str,
        default='releases.json'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path; by default updates the input file',
        nargs='?',
        type=str,
        default=None
    )
    parser.add_argument(
        '-d', '--dry-run',
        help='Show what would be updated without making changes',
        action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Enable verbose output',
        action='store_true'
    )

    return parser.parse_args()


# --- Data Processing Functions ---
def load_features_json(filepath: str) -> List[dict]:
    """
    Load the existing features.json file.

    Args:
        filepath: The path to the features.json file

    Returns:
        A List of feature dictionaries
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"Features file not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print_error(f"Error parsing features JSON: {e}")
        sys.exit(1)


def load_releases_json(filepath: str) -> List[dict]:
    """
    Load the releases.json file for version mapping.

    Args:
        filepath: The path to the releases.json file

    Returns:
        A List of release dictionaries
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"Releases file not found: {filepath}")
        print_error("The releases.json file is required for version-to-codename mapping")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print_error(f"Error parsing releases JSON: {e}")
        sys.exit(1)


def save_features_json(features: List[dict], filepath: str):
    """
    Save the updated features to a JSON file.

    Args:
        features: List of feature dictionaries
        filepath: Path to save the JSON file
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(features, f, indent=4)
            f.write('\n')  # Add trailing newline for consistency
    except IOError as e:
        print_error(f"Error writing features file: {e}")
        sys.exit(1)


def extract_feature_id_from_url(url: str) -> str:
    """
    Extract the feature ID from a wiki URL fragment.

    Args:
        url: URL fragment like "/Security/Features#feature-name"

    Returns:
        A feature ID string
    """
    if '#' in url:
        return url.split('#')[-1]
    return url.split('/')[-1]


def determine_state_from_style(style: str) -> str:
    """
    Determine the state based on the background color style.

    Args:
        style: CSS style string containing background-color

    Returns:
        A State string (DEFAULT, AVAILABLE, or UNIMPLEMENTED)
    """
    if not style:
        return 'UNIMPLEMENTED'

    # Determine the background color of the cell
    hex_match = re.search(r'#([0-9a-fA-F]{6})', style)

    if hex_match:
        hex_value = f"#{hex_match.group(1).lower()}"
        try:
            return STATE_COLOR_MAP[hex_value]
        except KeyError:
            print_error(f"Failed to match cell color to expected values")
            return 'UNIMPLEMENTED'

    return 'UNIMPLEMENTED'


def clean_text(text: str) -> str:
    """
    Clean and normalize text from HTML.

    Args:
        text: Raw text from HTML

    Returns:
        A cleaned text string
    """
    if not text:
        return ""

    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


# --- Web Scraping Functions ---
class WikiScraper:
    """Handles scraping of the Ubuntu Security Features wiki page."""

    def __init__(self, url: str, verbose: bool = False):
        self.url = url
        self.verbose = verbose
        self.soup = None
        self.releases = []
        self.features_data = {}
        self.version_map = {}

    def fetch_page(self) -> bool:
        """
        Fetch the wiki page content.

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.verbose:
                print_info(f"Fetching page from {self.url}...")

            response = requests.get(self.url, timeout=30)
            response.raise_for_status()


            self.soup = BeautifulSoup(response.text, 'html.parser')
            return True

        except requests.RequestException as e:
            print_error(f"Error fetching wiki page: {e}")
            return False

    def extract_releases(self) -> List[str]:
        """
        Extract release code names from the table header.

        Returns:
            A List of release code names
        """
        if not self.soup:
            return []

        # Find all tables on the page
        tables = self.soup.find_all('table')

        if self.verbose:
            print_info(f"Found {len(tables)} tables on the page")

        # The features table should be the third table on the page
        if len(tables) < 3:
            print_error(f"Expected at least 3 tables, but found {len(tables)}")
            return []

        features_table = tables[2]

        if self.verbose:
            rows = features_table.find_all('tr')
            print_info(f"Using third table with {len(rows)} rows")

        # Get the header row (first row of the table)
        header_row = features_table.find('tr')
        if not header_row:
            print_error("Could not find header row in features table")
            return []

        releases = []
        header_cells = header_row.find_all(['td', 'th'])

        if self.verbose:
            print_info(f"Header has {len(header_cells)} cells")
            for i, cell in enumerate(header_cells[:6]):
                text = clean_text(cell.get_text())
                print_info(f"Cell {i}: '{text}'")

        # Skip the first cell (feature name column)
        for cell in header_cells[1:]:
            releases.append(clean_text(cell.get_text()))

        if self.verbose:
            print_info(f"Found releases: {releases}")

        self.releases = releases
        return releases

    def extract_features(self) -> Dict[str, dict]:
        """
        Extract all features and their implementation status from the wiki.

        Returns:
            A dictionary mapping feature IDs to feature data
        """
        if not self.soup:
            return {}

        # Find the main features table
        table = self.soup.find_all('table')[2]
        if not table:
            return {}

        features = {}
        rows = table.find_all('tr')[1:]  # Skip header row

        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 2:
                continue

            # Extract feature information
            feature_cell = cells[0]
            feature_link = feature_cell.find('a')

            if not feature_link:
                continue

            # Get feature ID and label
            href = feature_link.get('href', '')
            feature_id = extract_feature_id_from_url(href)
            feature_label = clean_text(feature_link.get_text())

            if not feature_id:
                continue

            # Initialize feature data
            if feature_id not in features:
                features[feature_id] = {
                    'name': feature_id,
                    'label': feature_label,
                    'changes': {}
                }

            # Extract implementation status for each release
            for i, release in enumerate(self.releases):
                if i + 1 < len(cells):
                    status_cell = cells[i + 1]
                    style = status_cell.get('style', '')
                    comment = clean_text(status_cell.get_text())
                    state = determine_state_from_style(style)

                    # Map release version to code name if possible
                    release_code = self._version_to_codename(release)

                    if release_code and comment and comment != '--':
                        if release_code not in features[feature_id]['changes']:
                            features[feature_id]['changes'][release_code] = {}

                        features[feature_id]['changes'][release_code] = {
                            'comment': comment,
                            'state': state
                        }

        if self.verbose:
            print_info(f"Extracted {len(features)} features from wiki")

        self.features_data = features
        return features

    def set_version_map(self, releases: List[dict]):
        """
        Build version-to-codename mapping from releases data.

        Args:
            releases: List of release dictionaries from releases.json
        """
        self.version_map = {}
        for release in releases:
            # Extract version from human_name (e.g., "Ubuntu 22.04 LTS" -> "22.04 LTS")
            human_name = release.get('human_name', '')
            if human_name.startswith('Ubuntu '):
                version = human_name.replace('Ubuntu ', '')
                code_name = release.get('code_name', '')
                if version and code_name and not '/' in code_name:  # Skip ESM entries, they aren't on the wiki
                    self.version_map[version] = code_name

        if self.verbose:
            print_info(f"Loaded {len(self.version_map)} version mappings")

    def _version_to_codename(self, version: str) -> Optional[str]:
        """
        Convert Ubuntu version to codename.

        Args:
            version: Version string like "22.04 LTS"

        Returns:
            Codename string or None if not found
        """
        # Clean version string
        clean_version = version.strip()
        return self.version_map.get(clean_version)


# --- Update Functions ---
class FeaturesUpdater:
    """Handles updating the features.json file with wiki data."""

    def __init__(self, existing_features: List[dict], wiki_features: Dict[str, dict], 
                 verbose: bool = False):
        self.existing_features = existing_features
        self.wiki_features = wiki_features
        self.verbose = verbose
        self.updates_made = []
        self.new_features = []

    def update_features(self) -> List[dict]:
        """
        Update existing features with data from the wiki.

        Returns:
            Updated list of features
        """
        # Create a mapping of existing features by name
        existing_map = {}
        for feature in self.existing_features:
            if 'name' in feature:
                existing_map[feature['name']] = feature

        # Update existing features and track new ones
        for feature_id, wiki_data in self.wiki_features.items():
            if feature_id in existing_map:
                # Update existing feature
                self._update_existing_feature(existing_map[feature_id], wiki_data)
            else:
                # New feature found
                self._add_new_feature(wiki_data)

        # Add new features to the list
        updated_features = self.existing_features.copy()
        updated_features.extend(self.new_features)

        return updated_features

    def _update_existing_feature(self, existing: dict, wiki_data: dict):
        """
        Update an existing feature with wiki data.

        Args:
            existing: Existing feature dictionary
            wiki_data: Wiki feature data
        """
        updated = False

        # Update label if different
        if 'label' in wiki_data and existing.get('label') != wiki_data['label']:
            old_label = existing.get('label', 'None')
            existing['label'] = wiki_data['label']
            self.updates_made.append(f"Updated label for {existing['name']}: {old_label} -> {wiki_data['label']}")
            updated = True

        # Update changes
        if 'changes' not in existing:
            existing['changes'] = {}

        for release, impl_data in wiki_data.get('changes', {}).items():
            if release not in existing['changes']:
                # New release data
                existing['changes'][release] = impl_data
                self.updates_made.append(f"Added {release} data for {existing['name']}")
                updated = True
            else:
                # Check if implementation data changed
                existing_impl = existing['changes'][release]
                if (existing_impl.get('comment') != impl_data['comment'] or
                    existing_impl.get('state') != impl_data['state']):

                    old_data = f"{existing_impl.get('comment', 'None')} ({existing_impl.get('state', 'None')})"
                    new_data = f"{impl_data['comment']} ({impl_data['state']})"
                    existing['changes'][release] = impl_data
                    self.updates_made.append(f"Updated {release} for {existing['name']}: {old_data} -> {new_data}")
                    updated = True

        if updated and self.verbose:
            print_info(f"Updated feature: {existing['name']}")

    def _add_new_feature(self, wiki_data: dict):
        """
        Add a new feature from wiki data.

        Args:
            wiki_data: Wiki feature data
        """
        self.new_features.append(wiki_data)
        self.updates_made.append(f"Added new feature: {wiki_data['name']}")

        if self.verbose:
            print_info(f"New feature found: {wiki_data['name']}")

    def print_summary(self):
        """Print a summary of updates made."""
        if not self.updates_made:
            print_info("No updates needed! features.json is up to date.")
            sys.exit(1)
        else:
            print_info(f"\nUpdates made: {len(self.updates_made)}")
            for update in self.updates_made:
                print_info(f"  -- {update}")


# --- Script Entry Point ---
def main():
    # Parse command line arguments
    args = parse_arguments()

    # Load existing features
    if args.verbose:
        print_info(f"Loading features from {args.features}")
    existing_features = load_features_json(args.features)

    # Load releases for version mapping
    if args.verbose:
        print_info(f"Loading releases from {args.releases}")
    releases = load_releases_json(args.releases)

    # Scrape wiki page
    scraper = WikiScraper(WIKI_URL, args.verbose)
    scraper.set_version_map(releases)  # Set up version-to-codename mapping

    if not scraper.fetch_page():
        sys.exit(1)

    scraper.extract_releases()
    wiki_features = scraper.extract_features()

    if not wiki_features:
        print_error("No features extracted from wiki page")
        sys.exit(1)

    # Update features
    updater = FeaturesUpdater(existing_features, wiki_features, args.verbose)
    updated_features = updater.update_features()

    # Print summary
    updater.print_summary()

    # Save updates if not dry run
    if not args.dry_run:
        output_path = args.output or args.features
        if args.verbose:
            print_info(f"\nSaving updated features to {output_path}")
        save_features_json(updated_features, output_path)
        print_info(f"Successfully updated {output_path}")
    else:
        print_info("\nDry run -- no files were modified")


if __name__ == "__main__":
    main()
