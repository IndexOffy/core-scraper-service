"""
AWS Lambda handler for dotflow API.
"""

from mangum import Mangum

from app import create_app

app = create_app()

handler = Mangum(app, lifespan="off")


def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    This function is the entry point for AWS Lambda.
    It uses Mangum to adapt the FastAPI ASGI application to Lambda.
    """
    return handler(event, context)
