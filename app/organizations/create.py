import lib.model.organization as organizations
from lib.model.organization import Organization, ContactData
import lib.db.setup as db


def execute(name, contact_data_def):
    if name is None or len(name) == 0:
        return None

    definition = {}
    if contact_data_def is not None:
        contact_data = ContactData(**contact_data_def)
        definition = contact_data.to_d()
    definition[Organization.NAME] = name

    graph = db.init_graph("local")
    node = organizations.create(graph, definition)

    del node["uuid"]
    organization = Organization(**node)
    return organization.to_d()
