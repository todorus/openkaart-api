import app.lib.db.setup as db
from unittest import TestCase


TestCase.maxDiff = None


def wipe_db(graph):
    graph.data("MATCH (n) OPTIONAL MATCH (n)-[r]->(m) DELETE n,m,r")
