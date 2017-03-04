import lib.model.region as region
import lib.model.relations as relations
import lib.db.setup as db
import json
import logging
import geojson
from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union
from py2neo import Relationship


def execute(uuid, name=None, kind=None, childrenUuids=[]):
    hasName = name is not None and len(name) > 0
    hasKind = kind is not None and len(kind) > 0
    hasChildren = childrenUuids is not None and len(childrenUuids) > 0
    logging.warning("hasName %r hasKind %r hasChildren %r" % (hasName, hasKind, hasChildren))

    if not hasName and not hasKind and not hasChildren:
        return None

    graph = db.init_graph("local")

    node = region.find(graph, {"uuid": uuid})
    logging.warning('argcheck %r' % node)
    if node is None:
        logging.warning("illigal argument: unknown region %s" % uuid)
        return None

    changes = {}

    if hasName:
        changes["name"] = name
    if hasKind:
        changes["type"] = kind
    if hasChildren:
        children = []
        for uuid in childrenUuids:
            definition = {"uuid": uuid}
            child = region.find(graph, definition)
            if child is None:
                logging.warning("child not found %s" % uuid)
                return None
            child_geometry = geojson.loads(child["geometry"])
            child_shape = shape(child_geometry)
            children.append(child_shape)
        geometry = cascaded_union(children)
        mapped_geometry = mapping(geometry)
        changes["geometry"] = mapped_geometry

    logging.warning("changes: %s" % json.dumps(changes))

    tx = graph.begin(autocommit=False)
    if node is None:
        logging.warning("region not found %s" % uuid)
        return None

    if hasChildren:
        region.detachChildren(tx, uuid)

        for uuid in childrenUuids:
            child = region.find(tx, {"uuid": uuid})
            if child is None:
                logging.warning("child not found %s" % uuid)
                tx.rollback()
                return None
            rel = Relationship(child, relations.BELONGS_TO, node)
            tx.create(rel)
    node = region.update(tx, uuid, changes)

    tx.commit()

    node = region.find(graph, {"uuid": uuid})
    logging.warning("finished, returning %r" % node)
    return node
