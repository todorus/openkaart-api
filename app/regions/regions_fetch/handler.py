from __future__ import print_function
import json
import logging
import app.model.region as region
import app.db.setup as db


log = logging.getLogger()
log.setLevel(logging.INFO)

graph = db.init_graph("test")
databaseName = "test_database"


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    cursor = region.search(graph, databaseName, **event)
    return region.readCursor(cursor)
