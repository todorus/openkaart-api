import json
from app.db import setup as db
from app.model import region


def execute(graph, databaseName, fileName):
    data = json.load(open(fileName))
    for item in data:
        properties = {
            "name": item["properties"]["gemeentena"],
            "code": item["properties"]["code"],
            "geometry": item["geometry"],
        }

        if not region.exists(graph, databaseName, properties):
            region.create(graph, databaseName, properties)
            print properties["name"]
