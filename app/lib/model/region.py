from enum import Enum
from py2neo import Node, Relationship, NodeSelector
from py2neo.database import Transaction
import json
import uuid


ZIP = u"Zip"
POSTAL_AREA = u"PostalArea"
PLACE = u"Place"
MUNICIPALITY = u"Municipality"
PROVINCE = u"Province"
CARE = u"Care"


def __cleanDefinition(definition):
    # py2neo does not support dictionary properties, so convert it to json
    if 'geometry' in definition:
        definition["geometry"] = json.dumps(definition["geometry"])
    if 'uuid' not in definition:
        definition["uuid"] = str(uuid.uuid1())
    return definition


def new(graph, definition):
    definition = __cleanDefinition(definition)
    node = Node("Region", **definition)
    return node


def merge(graph, definition):
    node = new(graph, definition)
    return graph.merge(node)


def create(graph, definition):
    node = new(graph, definition)
    graph.create(node)
    return node


def createAll(graph, node_definitions):
    transaction = graph.begin()
    for definition in node_definitions:
        node = new(graph, definition)
        transaction.create(node)

    transaction.commit()


def update(graph, uuid, definition):
    node = find(graph, {"uuid": uuid})
    if node is None:
        return None

    definition["uuid"] = uuid
    __cleanDefinition(definition)
    for key, value in definition.iteritems():
        node[key] = value
    if isinstance(graph, Transaction):
        graph = graph.graph
    graph.push(node)
    return node


def delete(graph, definition):
    node = find(graph, definition)
    graph.delete(node)


def exists(graph, definition):
    return len(match(graph, definition)) > 0


def match(graph, definition):
    if "geometry" in definition:
        definition = dict(definition)
        del definition["geometry"]

    selector = NodeSelector(graph)
    result = list(selector.select("Region", **definition))
    return result


def find(graph, definition):
    results = match(graph, definition)
    if len(results) == 0:
        return None
    else:
        return results[0]


def search(graph, query=None, limit=10, page=1):
    skip = (page - 1) * limit

    result = None
    count = None
    if query is not None:
        query = '(?i)%s.*' % (query)

        result = graph.run(
            '''
            MATCH (n:Region)
            WHERE n.name =~ {query}
            RETURN n
            ORDER BY LOWER(n.name), length(n.name) ASC
            SKIP {skip}
            LIMIT {limit}
            ''',
            query=query, skip=skip, limit=limit
        )
        count = graph.run(
            '''
            MATCH (n:Region)
            WHERE n.name =~ {query}
            RETURN count(n) as count
            ''',
            query=query
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
        count = graph.run(
            '''
            MATCH (n:Region)
            RETURN count(n) as count
            '''
        )

    count = count.evaluate()
    return result, count


def children(graph, parentUuid, limit=10, page=1):
    skip = (page - 1) * limit

    result = graph.run(
        '''
        MATCH (c:Region)-[r:BELONGS_TO]->(p:Region)
        WHERE p.uuid = {parentUuid}
        RETURN c
        ORDER BY LOWER(c.name), length(c.name) ASC
        SKIP {skip}
        LIMIT {limit}
        ''',
        parentUuid=parentUuid, skip=skip, limit=limit
    )
    count = graph.run(
        '''
        MATCH (c:Region)-[r:BELONGS_TO]->(p:Region)
        WHERE p.uuid = {parentUuid}
        RETURN count(c) as count
        ''',
        parentUuid=parentUuid
    )
    count = count.evaluate()
    return result, count


def detachChildren(graph, parentUuid):
    graph.run(
        '''
        MATCH (c:Region)-[r:BELONGS_TO]->(p:Region)
        WHERE p.uuid = {parentUuid}
        DELETE r
        ''',
        parentUuid=parentUuid
    ).close()


def count(graph, query=None):
    if query is not None:
        count = graph.run(
            '''
            MATCH (n:Region)
            WHERE n.name =~ {query}
            RETURN count(n) as count
            ''',
            query=query
        )
    else:
        count = graph.run(
            '''
            MATCH (n:Region)
            RETURN count(n) as count
            '''
        )
    return count.evaluate()


def readCursor(cursor):
    data = []

    while cursor.forward():
        values = dict(cursor.current().values()[0])
        if 'geometry' in values:
            values["geometry"] = json.loads(values["geometry"])
        data.append(values)

    return data
