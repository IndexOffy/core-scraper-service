"""Main"""

from src.data import DataInput
from src.explorer import Explorer
from src.browsers.chrome import Chrome


def main():
    initial_data = []
    initial_data.append(DataInput(url="https://google.com"))
    initial_data.append(DataInput(url="https://fernandocelmer.com"))

    browser = Chrome(
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
