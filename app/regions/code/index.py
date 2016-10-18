from __future__ import print_function
import app.lib.model.region as region
import app.lib.model.pagination as pagination
import app.lib.db.setup as db


def execute(params):
    graph = db.init_graph("local")
    databaseName = "db"

    cursor = region.search(graph, databaseName, **params)
    data = region.readCursor(cursor)
    pages = pagination.paginate(len(data), **params)
    return {"data": data, "pages": pages}
