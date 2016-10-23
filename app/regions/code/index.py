from __future__ import print_function
import app.lib.model.region as region
import app.lib.model.pagination as pagination
import app.lib.db.setup as db


def execute(raw_params):
    raw_params = {
        "query": raw_params.get('q'),
        "limit": cast_to_int(raw_params.get('limit')),
        "page": cast_to_int(raw_params.get('page'))
    }
    params = dict((k, v) for k, v in raw_params.iteritems() if v is not None)

    graph = db.init_graph("local")

    cursor = region.search(graph, **params)
    data = region.readCursor(cursor)
    pages = pagination.paginate(len(data), **params)
    return {"data": data, "pages": pages}


def cast_to_int(value):
    if value is not None:
        value = int(value)

    return value
