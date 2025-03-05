#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008-2024 Canonical Ltd.
#  Author: Jamie Strandboge <jamie@ubuntu.com>
#  Author: Kees Cook <kees@ubuntu.com>
#  Author: Steve Beattie <steve.beattie@canonical.com>
#
# This script is distributed under the terms and conditions of the GNU General
# Public License, Version 3 or later. See http://www.gnu.org/copyleft/gpl.html
# for details.

from __future__ import print_function

import os

# nobody should be using ubuntu 14.04 LTS with this code, so we don't
# need a fallback implementation to ConfigObj
from configobj import ConfigObj

# private singleton object, use read_config() to access
_config = None


# _read_config: does the actual work without writing to the global
# singleton. This can be used in tests where read_config() will always
# return the same thing.
def _read_config(_config_file=None):

    if _config_file:
        config_file = _config_file
    else:
        config_file = os.path.join(
            os.path.expanduser("~"), ".ubuntu-cve-tracker.conf"
        )

    if not os.path.exists(config_file):
        raise ValueError("Could not find '%s'" % (config_file))

    config = ConfigObj(config_file)

    validate_config(config, config_file)

    return config


# _read_config_cached: if the results of parsing the config file have
# not already been cached, save it; otherwise return the singleton.
# Takes an optional config file path as an argument. This can be used in tests
# where read_config() will only use ~/.ubuntu-cve-tracker.conf
def _read_config_cached(_config_file=None):
    global _config

    # if we've already parsed the config file, return what we already
    # have
    if not _config:
        _config = _read_config()

    return _config


# read_uct_config: call with no arguments to get the contents of
# ~/.ubuntu-cve-tracker.conf
def read_uct_config():
    return _read_config_cached()


# XXX-FIXME this should use configobj's Validator stuff
def validate_config(config, config_file):

    # Validate required arguments
    if "plb_authentication" not in config:
        raise ValueError(("Could not find 'plb_authentication' entry in %s." % (config_file)))
    if not os.path.exists(config["plb_authentication"]):
        raise ValueError(("Could not find file specified by 'plb_authentication' in %s." % (config_file)))