import json
from app.model import region


def execute(graph, databaseName, fileName):
    data = json.load(open(fileName))
    for item in data:
        name = str(item["properties"]["PC4"])
        properties = {
            "name": name,
            "code": name,
            "type": region.ZIP,
            "geometry": item["geometry"],
        }

        query = {"code": properties["code"], "type": properties["type"]}
        if not region.exists(graph, databaseName, query):
            region.create(graph, databaseName, properties)
            print properties["name"]
