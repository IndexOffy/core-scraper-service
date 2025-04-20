"""Main"""

from dotflow import DotFlow

from source.tasks import (
    explore_outside,
    href_url_extractor,
    text_url_extractor
)


def main():
    initials = []
    workflow = DotFlow()

    for link in initials:
        workflow.task.add(
            step=[
                explore_outside,
                href_url_extractor,
                text_url_extractor
            ],
            initial_context=link
        )

    workflow.start()


if __name__ == '__main__':
    main()
