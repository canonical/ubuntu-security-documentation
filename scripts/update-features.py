#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2026 Canonical, Ltd.
# Author: Edwin Jiang <edwin.jiang@canonical.com>
# License: GPLv3

import argparse
import json
import logging
import sys
from bisect import insort

PROGRAM_NAME = "update-features"

logger = logging.getLogger(PROGRAM_NAME)
PROGRAM_DESCRIPTION = """
For a given release code name, attempt to add it to a change group for each
feature in features.json.  If the release is missing from a feature, it is
appended to the same change group as the preceding release (according to
release order in releases.json).  features.json is modified in place.
"""


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION,
    )
    parser.add_argument(
        "release",
        help="The release code name to add (e.g. 'questing')",
    )
    parser.add_argument(
        "-r",
        "--releases",
        help='Path to releases.json (default: "releases.json")',
        default="releases.json",
    )
    parser.add_argument(
        "-f",
        "--features",
        help='Path to features.json (default: "features.json")',
        default="features.json",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose logging (INFO level)",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug logging (DEBUG level)",
        action="store_true",
    )
    return parser.parse_args()


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def setup_logging(args: argparse.Namespace) -> None:
    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    else:
        level = logging.WARNING
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(name)s: %(levelname)s: %(message)s"))
    logger.setLevel(level)
    logger.addHandler(handler)


def main() -> None:
    args = parse_arguments()
    setup_logging(args)

    logger.debug("Loading releases from %s", args.releases)
    releases = load_json(args.releases)
    code_names = [r["code_name"] for r in releases]

    if args.release not in code_names:
        logger.error("Release '%s' not found in %s", args.release, args.releases)
        sys.exit(1)

    release_idx = code_names.index(args.release)
    if release_idx == 0:
        logger.error(
            "Release '%s' is the first release; "
            "there is no preceding release to inherit from",
            args.release,
        )
        sys.exit(1)

    preceding = code_names[release_idx - 1]
    logger.info("Preceding release: %s", preceding)

    logger.debug("Loading features from %s", args.features)
    features = load_json(args.features)

    updated = 0
    for feature in features:
        changes = feature.get("changes")
        if not changes:
            continue

        # Check if the release is already present in any change group.
        already_present = any(
            args.release in group["releases"] for group in changes
        )
        if already_present:
            logger.debug("Feature '%s': release already present, skipping", feature["name"])
            continue

        # Find the change group that contains the preceding release.
        target_group = None
        for group in changes:
            if preceding in group["releases"]:
                target_group = group
                break

        if target_group is None:
            logger.warning(
                "Feature '%s' has no change group for preceding release '%s'",
                feature["name"],
                preceding,
            )
            continue

        insort(target_group["releases"], args.release)
        updated += 1
        logger.info(
            "Feature '%s': added to group with state=%s, comment='%s'",
            feature["name"],
            target_group["state"],
            target_group["comment"],
        )

    save_json(args.features, features)
    logger.info("Updated %d feature(s) in %s", updated, args.features)


if __name__ == "__main__":
    main()
