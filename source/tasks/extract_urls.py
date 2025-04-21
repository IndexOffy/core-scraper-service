import re

from urllib.parse import urlparse

from bs4 import BeautifulSoup

from dotflow import action


ONION_DOMAIN = ".onion"
ONION_REGEX = r'(https?://)?[a-zA-Z0-9]{16,56}\.onion/?'


@action
def href_url_extractor(previous_context):
    source = previous_context.storage.source
    html = BeautifulSoup(source, "html.parser")

    hrefs = html.find_all("a")
    dumps = [
        url.get("href").rstrip('/')
        for url in hrefs
        if re.search(ONION_DOMAIN, url.get("href", ""))
    ]
    previous_context.storage.hrefs += dumps

    return previous_context.storage


@action
def text_url_extractor(previous_context):
    source = previous_context.storage.source
    html = BeautifulSoup(source, "html.parser")

    hrefs = html.find_all(string=re.compile(ONION_REGEX))

    for href in hrefs:
        new_href = href[0:href.find(ONION_DOMAIN)+6]

        if not urlparse(new_href).scheme:
            new_href = f"http://{new_href}"

        previous_context.storage.hrefs.append(new_href)

    return previous_context.storage
