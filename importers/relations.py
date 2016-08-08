import json
from app.model import region
from py2neo import Node, Relationship


def execute(graph, databaseName, fileName):
    data = json.load(open(fileName))
    for item in data:
        municipalityCode = item["Gemeentecode"]
        zipCode = item['Postcode']

        municipality = region.match(graph, databaseName, {"type": region.MUNICIPALITY, "code": municipalityCode})
        zipArea = region.match(graph, databaseName, {"type": region.ZIP, "code": zipCode})

        if len(municipality) > 0 and len(zipArea) > 0:
            ab = Relationship(municipality[0], "CONTAINS", zipArea[0])
            graph.create(ab)
            print ab
