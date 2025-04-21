from dotflow import action

from source.core.serializers.content import Content
from source.core.browsers.chrome import Chrome


@action
def explore_outside(previous_context):
    browser = Chrome()
    driver = browser.get_instance()
    driver.get(previous_context.storage)

    return Content(
        url=previous_context.storage,
        title=driver.title,
        source=driver.page_source
    )
