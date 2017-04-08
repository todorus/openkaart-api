import lib.model.organization as organization
import lib.db.setup as db


def execute(name, contact_data):
    if name is None or len(name) == 0:
        return None
    if contact_data is None:
        return None

    graph = db.init_graph("local")
    #TODO save phone,email and other contactdata as direct properties of the node
    definition = {
        "name": name,
        "contact_data": contact_data
    }
    node = organization.create(graph, definition)

    return node
