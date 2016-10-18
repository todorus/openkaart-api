from __future__ import print_function
import json
import app.lib.model.region as region
import app.lib.model.pagination as pagination
import app.lib.db.setup as db


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

    graph = db.init_graph("local")
    databaseName = "db"

    cursor = region.search(graph, databaseName, **event)
    data = region.readCursor(cursor)
    pages = pagination.paginate(len(data), **event)
    return {"data": data, "pages": pages}
