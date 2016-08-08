from enum import Enum
from py2neo import Graph, Node, Relationship, NodeSelector
import json


ZIP = "Zip"
PLACE = "Place"
MUNICIPALITY = "Municipality"
PROVINCE = "Province"
CARE = "Care"


def new(graph, databaseName, definition):
    # py2neo does not support dictionary properties, so convert it to json
    if 'geometry' in definition:
        definition["geometry"] = json.dumps(definition["geometry"])
    node = Node("Region", databaseName, **definition)
    return node


def create(graph, databaseName, definition):
    # py2neo does not support dictionary properties, so convert it to json
    if 'geometry' in definition:
        definition["geometry"] = json.dumps(definition["geometry"])
    node = new(graph, databaseName, definition)
    return graph.create(node)


def createAll(graph, databaseName, node_definitions):
    transaction = graph.begin()
    for definition in node_definitions:
        node = new(graph, databaseName, definition)
        transaction.create(node)

    transaction.commit()


def exists(graph, databaseName, query):
    selector = NodeSelector(graph)
    result = list(selector.select("Region", databaseName, **query))
    return len(result) > 0


def search(graph, databaseName, query=None, limit=10, page=0):
    skip = page * limit

    result = None
    if query is None:
        result = graph.run(
            '''
            MATCH (n:Region)
            WHERE n.name =~ '(?i){query}.*'
            RETURN n
            ORDER BY LOWER(n.name), length(n.name) ASC
            SKIP {skip}
            LIMIT {limit}
            ''',
            query=query, skip=skip, limit=limit
        )
    else:
        result = graph.run(
            '''
            MATCH (n:Region)
            RETURN n
            ORDER BY LOWER(n.name), length(n.name) ASC
            SKIP {skip}
            LIMIT {limit}
            ''',
            skip=skip, limit=limit
        )
    return result


def readCursor(cursor):
    data = []

    while cursor.forward():
        values = dict(cursor.current().values()[0])
        if 'geometry' in values:
            values["geometry"] = json.loads(values["geometry"])
        data.append(values)

    return data
