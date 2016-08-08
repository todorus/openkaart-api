import importers.municipalities as municipalities
from app.db import setup as db
from app.model import region

graph = db.init_graph("local")
databaseName = "local_database"


def wipe_db(graph, databaseName):
    graph.data("MATCH (n:"+databaseName+") OPTIONAL MATCH (n:"+databaseName+")-[r]->(m) DELETE n,m,r")


municipalities.execute(graph, databaseName, "data/gemeentes.geo.json")
