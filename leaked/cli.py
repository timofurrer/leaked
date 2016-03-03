# -*- coding: utf-8 -*-

import click

@click.group()
def cli():
    """Find leaked information in different kind of services."""
    pass


main = cli
