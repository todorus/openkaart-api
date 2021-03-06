from __future__ import print_function
import lib.model.region as region
import lib.model.pagination as pagination
import lib.db.setup as db


def execute(raw_params):
    raw_params = {
        "query": raw_params.get('q'),
        "limit": cast_to_int(raw_params.get('limit')),
        "page": cast_to_int(raw_params.get('page'))
    }
    params = dict((k, v) for k, v in raw_params.iteritems() if v is not None)

    graph = db.init_graph("local")

    cursor, count = region.search(graph, **params)
    data = region.readCursor(cursor)
    pages = pagination.paginate(count, **params)
    return {"data": data, "pages": pages}


def cast_to_int(value):
    if value is not None:
        value = int(value)

    return value
