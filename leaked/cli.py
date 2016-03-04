# -*- coding: utf-8 -*-

"""
    Command-Line-Interface for leaked.
"""

import click

from .providers import available_providers, get_provider
from .modules import available_modules, get_module
from .requests import get_search_results


@click.group()
def cli():
    """Find leaked information in different kind of sources."""
    pass


@cli.command()
@click.option("-p", "--provider", type=click.Choice(available_providers.keys()),
              help="Specify the provider for the query")
@click.option("-m", "--module", required=True,
              type=click.Choice(available_modules.keys()),
              help="Specify the modules to search for")
@click.pass_context
def gather(ctx, provider, module):
    """Gather information from a provider."""
    provider = get_provider(provider)

    module = get_module(module)
    query_url = provider.build_module_query_url(module)

    click.echo("[*] Querying {0} for inventory...".format(click.style(query_url, bold=True)))
    raw_results = get_search_results([query_url])[0]
    pages = provider.get_amount_of_pages(raw_results)
    click.echo("==> Found {0} pages".format(click.style(str(pages), bold=True)))
    answer = click.prompt("Which pages do you want to analyse?", default="ALL")
    if answer == "ALL":
        pages_to_analyse = list(range(1, pages + 1))
    else:
        pages_to_analyse = [int(p.strip()) for p in answer.split()]

    # get all pages
    result_pages = get_search_results([provider.build_module_query_url(module, p) for p in pages_to_analyse],
                                     with_progress_bar=True,
                                     description="Get all requested pages")


    result_index = 1
    for result_page, page_index in zip(result_pages, pages_to_analyse):
        # get provider search results and parse them
        results = provider.parse(result_page, module, page_index)

        for result in results:
            click.secho("== Result #{0} ==".format(result_index), fg="magenta")

            click.secho("User: ", fg="cyan", bold=True, nl=False)
            click.secho(result["user"], fg="cyan")
            click.secho("Repository: ", fg="cyan", bold=True, nl=False)
            click.secho(result["repository"], fg="cyan")
            click.secho("Filename: ", fg="cyan", bold=True, nl=False)
            click.secho(result["filename"], fg="cyan")
            click.secho("URL: ", fg="cyan", bold=True, nl=False)
            click.secho(result["fileurl"], fg="cyan")
            click.secho("Data: ", fg="cyan", bold=True)
            for name, value in result["variables"].items():
                click.secho("    {0}: ".format(name), fg="yellow", bold=True, nl=False)
                click.secho(value, fg="red", bold=True)

            click.echo()
            result_index += 1

@cli.command()
@click.pass_context
def providers(ctx):
    """Show all available providers."""
    click.echo(" ".join(available_providers))


@cli.command()
@click.pass_context
def modules(ctx):
    """Show all available modules."""
    click.echo(" ".join(available_modules))


main = cli  # pylint: disable=invalid-name
