import importers.municipalities as municipalities
import importers.provinces as provinces
import importers.postal_areas as postal_areas
from app.db import setup as db
from app.model import region

graph = db.init_graph("local")
databaseName = "local_database"


def wipe_db(graph, databaseName):
    graph.data("MATCH (n:"+databaseName+") OPTIONAL MATCH (n:"+databaseName+")-[r]->(m) DELETE n,m,r")


wipe_db(graph, databaseName)
# municipalities.execute(graph, databaseName, "data/gemeentes.geo.json")
# provinces.execute(graph, databaseName, "data/provincies.geo.json")
postal_areas.execute(graph, databaseName, "data/postcodes.geo.json")
