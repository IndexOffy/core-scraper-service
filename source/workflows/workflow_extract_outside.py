"""Main"""

from dotflow import DotFlow

from source.tasks import (
    explore_outside,
    href_url_extractor,
    text_url_extractor
)


def workflow_extract_outside():
    context = "https://www.deepwebsiteslinks.com/deep-web-links/"

    workflow = DotFlow()
    workflow.task.add(
        step=[
            explore_outside,
            href_url_extractor,
            text_url_extractor
        ],
        initial_context=context
    )

    return workflow
