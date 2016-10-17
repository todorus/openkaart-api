import app.lib.db.setup as db
from unittest import TestCase


TestCase.maxDiff = None


def wipe_db(graph, databaseName):
    graph.data("MATCH (n:"+databaseName+") OPTIONAL MATCH (n:"+databaseName+")-[r]->(m) DELETE n,m,r")
