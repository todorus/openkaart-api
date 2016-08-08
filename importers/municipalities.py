import json
from app.model import region


def execute(graph, databaseName, fileName):
    data = json.load(open(fileName))
    for item in data:
        properties = {
            "name": item["properties"]["gemeentena"],
            "code": item["properties"]["code"],
            "type": region.MUNICIPALITY,
            "geometry": item["geometry"],
        }

        query = {"name": properties["name"], "type": properties["type"], "code": properties["code"]}
        if not region.exists(graph, databaseName, query):
            region.create(graph, databaseName, properties)
            print properties["name"]
