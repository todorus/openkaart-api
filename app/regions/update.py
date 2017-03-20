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
        for childUuid in childrenUuids:
            logging.warning("finding child1 %r" % {"uuid": childUuid})
            definition = {"uuid": childUuid}
            child = region.find(graph, definition)
            if child is None:
                logging.warning("child not found %s" % childUuid)
                return None
            child_geometry = geojson.loads(child["geometry"])
            child_shape = shape(child_geometry)
            children.append(child_shape)
        geometry = cascaded_union(children)
        mapped_geometry = mapping(geometry)
        changes["geometry"] = mapped_geometry

    logging.warning("changes: %s" % json.dumps(changes))

    # if hasChildren:
    #     region.detachChildren(graph, uuid)
    #
    #     for childUuid in childrenUuids:
    #         logging.warning("finding child2 %r" % {"uuid": childUuid})
    #         child = region.find(graph, {"uuid": childUuid})
    #         rel = Relationship(child, relations.BELONGS_TO, node)
    #         graph.create(rel)
    # node = region.update(graph, uuid, changes)

    # FIXME use a transaction
    if node is None:
        logging.warning("region not found %s" % uuid)
        return None

    if hasChildren:
        region.detachChildren(graph, uuid)

        for childUuid in childrenUuids:
            logging.warning("finding child2 %r" % {"uuid": childUuid})
            child = region.find(graph, {"uuid": childUuid})
            if child is None:
                logging.warning("child not found %s" % childUuid)
                # FIXME rollback
                return None
            rel = Relationship(child, relations.BELONGS_TO, node)
            graph.create(rel)
            logging.warning("created child2 rel")
    logging.warning("going to update %r" % changes)
    node = region.update(graph, uuid, changes)
    logging.warning("updated")

    node = region.find(graph, {"uuid": uuid})
    logging.warning("finished, returning %r" % node)
    return node
