"""Main"""

from dotflow import DotFlow

from source.tasks import (
    explore_outside,
    href_url_extractor,
    text_url_extractor,
    initial_data,
    storage_data
)


def main():
    workflow = DotFlow()
    workflow.task.add(
        step=[
            initial_data,
            explore_outside,
            href_url_extractor,
            text_url_extractor,
            storage_data
        ]
    )

    workflow.start()


if __name__ == '__main__':
    main()
