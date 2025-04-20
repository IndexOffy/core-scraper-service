from dotflow import action

from source.serializers.content import Content
from source.browsers.chrome import Chrome


@action
def explore_outside(initial_context):
    browser = Chrome()

    driver = browser.get_instance()
    driver.get(initial_context.storage)

    return Content(
        url=initial_context.storage,
        title=driver.title,
        source=driver.page_source
    )
