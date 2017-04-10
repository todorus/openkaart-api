from enum import Enum
from py2neo import Node, Relationship, NodeSelector
from py2neo.database import Transaction
import uuid


class ContactData():

    PHONE = "phone"
    ADDRESS = "address"
    EMAIL = "email"

    def __init__(self, phone=None, email=None, address=None):
        self.phone = phone
        self.email = email
        self.address = address

    def to_d(self):
        d = {}
        if self.phone is not None:
            d[ContactData.PHONE] = self.phone
        if self.email is not None:
            d[ContactData.EMAIL] = self.email
        if self.address is not None:
            d[ContactData.ADDRESS] = self.address

        return d


class Organization():

    NAME = "name"
    CONTACT_DATA = "contact_data"

    def __init__(self, name=None, **contact_data_args):
        self.name = name
        self.contact_data = ContactData(**contact_data_args)

    def to_d(self):
        return {
            Organization.NAME: self.name,
            Organization.CONTACT_DATA: self.contact_data.to_d()
        }


def __cleanDefinition(definition):
    if 'uuid' not in definition:
        definition["uuid"] = str(uuid.uuid1())
    return definition


def new(graph, definition):
    definition = __cleanDefinition(definition)
    node = Node("Organization", **definition)
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
    selector = NodeSelector(graph)
    result = list(selector.select("Organization", **definition))
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
            MATCH (n:Organization)
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
            MATCH (n:Organization)
            WHERE n.name =~ {query}
            RETURN count(n) as count
            ''',
            query=query
        )
    else:
        result = graph.run(
            '''
            MATCH (n:Organization)
            RETURN n
            ORDER BY LOWER(n.name), length(n.name) ASC
            SKIP {skip}
            LIMIT {limit}
            ''',
            skip=skip, limit=limit
        )
        count = graph.run(
            '''
            MATCH (n:Organization)
            RETURN count(n) as count
            '''
        )

    count = count.evaluate()
    return result, count


def children(graph, parentUuid, limit=10, page=1):
    skip = (page - 1) * limit

    result = graph.run(
        '''
        MATCH (c:Organization)-[r:BELONGS_TO]->(p:Organization)
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
        MATCH (c:Organization)-[r:BELONGS_TO]->(p:Organization)
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
        MATCH (c:Organization)-[r:BELONGS_TO]->(p:Organization)
        WHERE p.uuid = {parentUuid}
        DELETE r
        ''',
        parentUuid=parentUuid
    ).close()


def count(graph, query=None):
    if query is not None:
        count = graph.run(
            '''
            MATCH (n:Organization)
            WHERE n.name =~ {query}
            RETURN count(n) as count
            ''',
            query=query
        )
    else:
        count = graph.run(
            '''
            MATCH (n:Organization)
            RETURN count(n) as count
            '''
        )
    return count.evaluate()


def readCursor(cursor):
    data = []

    while cursor.forward():
        values = dict(cursor.current().values()[0])
        data.append(values)

    return data
