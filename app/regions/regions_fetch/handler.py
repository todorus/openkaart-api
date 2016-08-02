from __future__ import print_function
import json
import logging
import app.model.region as region
import app.model.pagination as pagination
import app.db.setup as db


log = logging.getLogger()
log.setLevel(logging.INFO)

graph = db.init_graph("test")
databaseName = "test_database"


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # if (event.limit != undefined && event.limit != null) {
    # limit = event.limit > 0 ? event.limit : limit;
    #
    #     if(event.page != undefined && event.page != null) {
    #       var eventPage = parseInt(event.page);
    #       page = eventPage >= 0 ? eventPage : page;
    #     }
    #   }

    cursor = region.search(graph, databaseName, **event)
    data = region.readCursor(cursor)
    pages = pagination.paginate(len(data), **event)
    return {"data": data, "pages":pages}
