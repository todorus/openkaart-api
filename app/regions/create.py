import lib.model.region as region
import lib.db.setup as db
import json


def execute(name, type, childrenUuids=[]):
    if childrenUuids is None:
        return None

    graph = db.init_graph("local")

    children = []
    for uuid in childrenUuids:
        definition = {"uuid": uuid}
        child = region.find(graph, definition)
        if child is None:
            return None

        children.push(child)

    return {}
