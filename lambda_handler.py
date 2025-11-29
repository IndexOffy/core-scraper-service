"""
AWS Lambda handler for indexoffy API.
"""

import asyncio

from mangum import Mangum

from app import create_app

app = create_app()

handler = Mangum(app, lifespan="off")


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return handler(event, context)
