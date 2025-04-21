from os import environ

from dotflow import action
from dotenv import load_dotenv

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from source.core.serializers.content import Content


@action
def storage_data(previous_context):
    load_dotenv()

    client = MongoClient(
        environ.get("NOSQL_DATABASE_URL"),
        server_api=ServerApi('1')
    )
    collection = client["indexoffy"]["onion"]

    dataset = [
        Content(url=href).model_dump()
        for href in previous_context.storage.hrefs
    ]
    collection.insert_many(dataset)

    for href in previous_context.storage.hrefs:
        print(href)
