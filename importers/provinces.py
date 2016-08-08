import json
from app.model import region


def execute(graph, databaseName, fileName):
    data = json.load(open(fileName))
    for item in data:
        properties = {
            "name": item["properties"]["Provincien"].replace("-", " "),
            "type": region.PROVINCE,
            "geometry": item["geometry"],
        }

        query = {"name": properties["name"], "type": properties["type"]}
        if not region.exists(graph, databaseName, query):
            region.create(graph, databaseName, properties)
            print properties["name"]
