import lib.model.region as region
import lib.model.relations as relations
import lib.db.setup as db
import json
import geojson
from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union
from py2neo import Relationship


def execute(uuid, name=None, kind=None, childrenUuids=[]):
    hasName = name is not None and len(name) > 0
    hasKind = kind is not None and len(kind) > 0
    hasChildren = childrenUuids is not None and len(childrenUuids) > 0
    if not hasName and not hasKind and not hasChildren:
        return None

    graph = db.init_graph("local")

    changes = {}

    if hasName:
        changes["name"] = name
    if hasKind:
        changes["kind"] = kind
    if hasChildren:
        children = []
        for uuid in childrenUuids:
            definition = {"uuid": uuid}
            child = region.find(graph, definition)
            if child is None:
                return None
            child_geometry = geojson.loads(child["geometry"])
            child_shape = shape(child_geometry)
            children.append(child_shape)
        geometry = cascaded_union(children)
        mapped_geometry = mapping(geometry)
        changes["geometry"] = mapped_geometry

    tx = graph.begin(autocommit=False)
    node = region.update(tx, uuid, changes)
    if node is None:
        return None

    if hasChildren:
        # TODO remove existing relations
        region.detachChildren(tx, uuid)

        for uuid in childrenUuids:
            child = region.find(tx, {"uuid": uuid})
            if child is None:
                tx.rollback()
                return None
            rel = Relationship(child, relations.BELONGS_TO, node)
            tx.create(rel)

    tx.commit()

    node = region.find(graph, uuid)
    return node
