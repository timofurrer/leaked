leaked
======
|pypi| |license|

**leaked** is a toolkit to find sensitive and security relevant information in different kind of sources.

These *sources* are implemented as extensible *adapters*. In order to find sensitive information in these *adapters*
there are a bunch of *modules*. Each *module* contains information to the according service the information belongs to
and one or more search terms.

**Examples for Adapters are**:

- GitHub
- Local Repository

**Examples for Modules are**:

- FTP
- WordPress
- RSA private keys
- System Credentials

Features
--------

- A beautiful command-line interface thanks to click.
- Implemented to be easily extensible.
- ...

Documentation
-------------

Coming soon.

License
-------

**leaked** is released under the MIT License. See the bundled LICENSE file for details.


.. |pypi| image:: https://img.shields.io/pypi/v/leaked.svg?style=flat&label=version
    :target: https://pypi.python.org/pypi/leaked
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://raw.githubusercontent.com/timofurrer/leaked/master/LICENSE
    :alt: Package license
