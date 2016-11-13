from __future__ import print_function
import lib.model.region as region
import lib.model.pagination as pagination
import lib.db.setup as db
import json


def execute(uuid):

    graph = db.init_graph("local")
    result = region.find(graph, {"uuid": uuid})
    if result is not None:
        result = dict(result)
        result["geometry"] = json.loads(result["geometry"])
    return result
