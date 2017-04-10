import lib.model.organization as organizations
import lib.db.setup as db


def execute(definition):
    graph = db.init_graph("local")
    if not organizations.exists(graph, definition):
        return None
    organizations.delete(graph, definition)

    return True
