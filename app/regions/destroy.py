import lib.model.region as region
import lib.db.setup as db


def execute(definition):
    graph = db.init_graph("local")
    if not region.exists(graph, definition):
        return None
    region.delete(graph, definition)

    return True
