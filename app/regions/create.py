import lib.model.region as region
import lib.db.setup as db
import json


def execute(name, kind, childrenUuids=[]):
    if name is None or len(name) == 0:
        return None
    if kind is None or len(kind) == 0:
        return None
    if childrenUuids is None or len(childrenUuids) == 0:
        return None

    graph = db.init_graph("local")

    children = []
    for uuid in childrenUuids:
        definition = {"uuid": uuid}
        child = region.find(graph, definition)
        if child is None:
            return None

        children.append(child)

    #TODO append child geometries
    #TODO create the region
    #TODO return the region

    return {}
