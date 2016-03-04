# -*- coding: utf-8 -*-

"""
    This module contains all modules for `leaked`.
"""

import os
import yaml

from .errors import LeakedError

def get_modules():
    """Get all available modules"""
    basepath = os.path.join(os.path.dirname(__file__), "modules")
    return {os.path.splitext(os.path.basename(path))[0]: os.path.join(basepath, path) for path in os.listdir(basepath)}

available_modules = get_modules()


def parse_module(path):
    """Parse the given module file."""
    with open(path) as module_file:
        return yaml.load(module_file)


def get_module(name):
    """Get the module with the given name."""
    try:
        return parse_module(available_modules[name.lower()])
    except KeyError:
        raise LeakedError("No such module available: {0}".format(name))
