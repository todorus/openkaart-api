from enum import Enum
from py2neo import Graph, Node, Relationship, NodeSelector
import bcrypt
import uuid
import logging

class User:
    """Represents a user"""
    def __init__(self, username=None, password=None, authenticated=False, active=False, anonymous=False, uuid=None):
        self.username = username
        self.password = password
        self.is_authenticated = authenticated
        self.is_active = active
        self.is_anonymous = anonymous
        self.uuid = uuid

    def get_id(self):
        return self.uuid


def __cleanDefinition(definition):
    if 'uuid' not in definition:
        definition["uuid"] = str(uuid.uuid1())
    if 'password' not in definition:
        raise ValueError("User must be created with a password")

    definition["password"] = crypt(definition["password"])
    return definition


def new(graph, definition):
    definition = __cleanDefinition(definition)
    node = Node("User", **definition)
    return node


def merge(graph, definition):
    node = new(graph, definition)
    return graph.merge(node)


def create(graph, definition):
    node = new(graph, definition)
    graph.create(node)
    return __nodeToUser(node)


def createAll(graph, node_definitions):
    nodes = []
    transaction = graph.begin()
    for definition in node_definitions:
        node = new(graph, definition)
        transaction.create(node)
        nodes.append(node)

    transaction.commit()
    return __nodesToUsers(nodes)


def exists(graph, definition):
    return len(match(graph, definition)) > 0


def match(graph, definition):
    selector = NodeSelector(graph)
    nodes = list(selector.select("User", **definition))
    return __nodesToUsers(nodes)


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
            MATCH (n:User)
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
            MATCH (n:User)
            WHERE n.name =~ {query}
            RETURN count(n) as count
            ''',
            query=query
        )
    else:
        result = graph.run(
            '''
            MATCH (n:User)
            RETURN n
            ORDER BY LOWER(n.name), length(n.name) ASC
            SKIP {skip}
            LIMIT {limit}
            ''',
            skip=skip, limit=limit
        )
        count = graph.run(
            '''
            MATCH (n:User)
            RETURN count(n) as count
            '''
        )

    count = count.evaluate()
    users = __nodesToUsers(result)
    return users, count


def login(graph, username, password):
    user = find(graph, {"username": username.encode("utf-8")})
    if user is None:
        logging.warning("no user found with name %s" % username)
        return None
    elif not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        logging.warning("password does not match with that of %s" % username)
        return None
    else:
        return User(uuid=user.uuid, username=user.username, authenticated=True, active=True)


def crypt(password):
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt(14))


def __nodeToUser(node):
    converted = dict(node)
    kwargs = {
        "uuid": converted["uuid"],
        "username": converted["username"],
        "password": converted["password"],
        "active": True
    }
    return User(**kwargs)


def __nodesToUsers(nodes):
    users = []
    for node in nodes:
        users.append(__nodeToUser(node))
    return users
