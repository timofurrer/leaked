# -*- coding: utf-8 -*-

"""
    This module contains all modules for `leaked`.
"""

from .errors import LeakedError


# TODO: parse from yaml config files
available_modules = {
    "wordpress": {
        "filename": "wp-config",
        "extension": "php",
        "searchterm": "FTP_PASS",
        "variables": [
            "FTP_HOST", "FTP_USER", "FTP_PASS",
            "DB_HOST", "DB_USER", "DB_PASS", "DB_NAME"
        ],
        "variable_regex": """{0}['"]\s*,\s*['"](.*?)['"]"""
    }
}


def get_module(name):
    """Get the module with the given name."""
    try:
        return available_modules[name.lower()]
    except KeyError:
        raise LeakedError("No such module available: {0}".format(name))
