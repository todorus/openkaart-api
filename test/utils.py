import app.db.setup as db

def wipe_db(graph, databaseName):
    graph.data("MATCH (n:"+databaseName+") OPTIONAL MATCH (n:"+databaseName+")-[r]->(m) DELETE n,m,r")
