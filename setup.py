# -*- coding: utf-8 -*-

"""
    Setup leaked python package.

    Only support Python versions > 3.4.1
"""

import ast
import re
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 4, 1):
    raise RuntimeError("twtxt requires Python 3.4.1+")


def get_version():
    """Gets the current version"""
    _version_re = re.compile(r"__VERSION__\s+=\s+(.*)")
    with open("leaked/__init__.py", "rb") as init_file:
        version = str(ast.literal_eval(_version_re.search(
            init_file.read().decode("utf-8")).group(1)))
    return version


setup(
    name="leaked",
    version=get_version(),
    license="MIT",

    description="Find leaked information in different kind of services",
    long_description=open("./README.rst", "r", encoding="utf-8").read(),

    author="Timo Furrer",
    author_email="tuxtimo@gmail.com",

    url="https://github.com/timofurrer/leaked",

    packages=find_packages(),
    include_package_data=True,

    install_requires=[],

    entry_points={
        "console_scripts": ["leaked=leaked.cli:main"]
    },

    keywords=[
        "leaked",
        "credentials", "passwords",
        "security",
        "git", "github",
        "source", "code",
        "sensitive", "information"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
    ],
)
