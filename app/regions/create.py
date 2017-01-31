import lib.model.region as region
import lib.db.setup as db
import json
import geojson
from geojson import Feature
from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union


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
        child_geometry = geojson.loads(child["geometry"])
        child_shape = shape(child_geometry)
        children.append(child_shape)
    geometry = cascaded_union(children)
    mapped_geometry = mapping(geometry)

    definition = {
        "geometry": mapped_geometry,
        "name": name,
        "type": kind
    }
    node = region.create(graph, definition)

    result = {
        u"uuid": node["uuid"],
        u"name": node["name"],
        u"type": node["type"],
        u"geometry": json.loads(node["geometry"])
    }
    return result
