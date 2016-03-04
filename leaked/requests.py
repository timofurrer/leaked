# -*- coding: utf-8 -*-

"""
    Utilities to request the API data from provider searches.
"""


import tqdm
import asyncio
import aiohttp
import random

__USER_AGENTS__ = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
]


@asyncio.coroutine
def get_search_result(client, query):
    """Get the search result for one query."""
    response = yield from client.get(query)
    try:
        content = yield from response.text()
    except UnicodeDecodeError:
        # FIXME: why does this happen and how to prevent?
        return ""
    return content


@asyncio.coroutine
def process_search(client, queries, with_progress_bar=False, description=None):
    """Process the search for all queries."""
    coroutines = [get_search_result(client, query) for query in queries]

    results = []
    if with_progress_bar:
        for coroutine in tqdm.tqdm(asyncio.as_completed(coroutines), desc=description, total=len(coroutines)):
            content = yield from coroutine
            results.append(content)
    else:
        for coroutine in asyncio.as_completed(coroutines):
            content = yield from coroutine
            results.append(content)
    return results


def get_search_results(queries, with_progress_bar=False, description=None):
    """Get search results from the given queries."""
    connector = aiohttp.TCPConnector()
    headers = {"User-Agent": random.choice(__USER_AGENTS__)}
    with aiohttp.ClientSession(connector=connector, headers=headers) as client:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(process_search(client, queries, with_progress_bar, description))
    return result
