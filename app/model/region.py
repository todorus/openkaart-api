from enum import Enum
from py2neo import Graph, Node, Relationship
import json


ZIP = "Zip"
PLACE = "Place"
MUNICIPALITY = "Municipality"
PROVINCE = "Province"
CARE = "Care"


def createAll(graph, databaseName, node_definitions):
    transaction = graph.begin()
    for definition in node_definitions:
        # py2neo does not support dictionary properties, so convert it to json
        if 'geometry' in definition:
            definition["geometry"] = json.dumps(definition["geometry"])

        node = Node("Region:"+databaseName, **definition)
        transaction.create(node)

    transaction.commit()
