"""
Initial Module
"""

from dataclasses import dataclass
from typing import List, Optional

from data import DataInput
from explorer import Explorer
from browser import BrowserChrome


def main():
    initial_data = []
    initial_data.append(DataInput(url="https://google.com"))
    initial_data.append(DataInput(url="https://fernandocelmer.com"))

    browser = BrowserChrome(
        headless=False,
        multi_instances=True
    )

    explorer = Explorer(
        data=initial_data,
        browser=browser,
    )

    explorer.get()
    for data in explorer.data:
        print(data.title)


if __name__ == '__main__':
    main()
