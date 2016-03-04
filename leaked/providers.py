# -*- coding: utf-8 -*-

"""
    This module contains all providers for leaked.
"""

import re
from bs4 import BeautifulSoup
from collections import namedtuple

from .errors import LeakedError
from .requests import get_search_results


class Provider(object):
    """Base class for all providers."""

    def __init__(self, name):
        self.name = name

    def build_module_query_url(self, module):
        """Build query URL with the given module data."""
        pass

    def build_term_query_url(self, searchterm):
        """Build query URL with the given searchterm."""
        pass

    def parse(self, data):
        """Parse given query result data."""
        pass


class GitHubProvider(Provider):
    """
        Provider to gather information from
        GitHub hosted repositories.
    """
    BASE_URL = "https://github.com"
    QUERY_URL = BASE_URL + "/search?type=code&q="

    CodeListItem = namedtuple("CodeListItem", ["user", "repository", "filename", "fileurl"])

    def __init__(self):
        super(GitHubProvider, self).__init__("GitHub")

    def build_module_query_url(self, module, page=1):
        query_terms = []
        if "filename" in module:
            query_terms.append("filename:{0}".format(module["filename"]))
        if "extension" in module:
            query_terms.append("extension:{0}".format(module["extension"]))
        if "path" in module:
            query_terms.append("path:{0}".format(module["path"]))

        query = "{0} {1}".format(" ".join(query_terms), module["searchterm"])
        return self.QUERY_URL + query.replace(" ", "+") + "&p={0}".format(page)

    def _check_abuse(self, soup):
        """Get if abuse detection mechanism was triggered"""
        abuse_msg = soup.select("html body div p")[0]
        if abuse_msg and abuse_msg.text.startswith("You have triggered an abuse detection mechanism"):
            raise LeakedError("GitHub has a problem: You have triggered an abuse detection mechanism. Wait a few minutes and try again.")

    def get_amount_of_pages(self, data):
        soup = BeautifulSoup(str(data), "html.parser")
        # self._check_abuse(soup)
        pagination = soup.find("div", {"class": "pagination"})
        pages = pagination.find_all("a")
        if len(pages) > 2:
            return int(pages[-2].text)
        return 1

    def parse(self, data, module, page_index):
        soup = BeautifulSoup(str(data), "html.parser")
        # self._check_abuse(soup)
        code_list_items = soup.find_all("div", {"class": "code-list-item"})
        code_items = [self._parse_code_list_item(i) for i in code_list_items]

        # get all source files from code items and find variables
        raw_source_file_contents = get_search_results((i.fileurl for i in code_items),
                                                      with_progress_bar=True,
                                                      description="Get results of page {0}".format(page_index))

        results = []
        for item, content in zip(code_items, raw_source_file_contents):
            result = {
                "user": item.user, "repository": item.repository,
                "filename": item.filename, "fileurl": item.fileurl,
            }
            matches = {}
            for variable in module["variables"]:
                pattern = re.compile(module["variable_regex"].format(variable))
                # print(pattern)
                # print(content)
                match = pattern.search(content)
                if match:
                    value = match.group(1)
                    if value:
                        matches[variable] = value

            if matches:
                result["variables"] = matches
                results.append(result)
        return results

    def _parse_code_list_item(self, item):
        """Parse given code list item."""
        title = item.find("p", {"class": "title"})
        repository, sourcefile = title.find_all("a")

        user, repository = repository.text.split("/", maxsplit=1)
        filename = sourcefile.text
        fileurl = self.BASE_URL + sourcefile.get("href").replace("blob", "raw")
        return self.CodeListItem(user, repository, filename, fileurl)


available_providers = {
    "github": GitHubProvider()
}


def get_provider(name):
    """Returns the provider with the given name."""
    try:
        return available_providers[name.lower()]
    except KeyError:
        raise LeakedError("No such provider available: {0}".format(name))
