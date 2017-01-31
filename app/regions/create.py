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
        # child_feature = Feature(geometry=child_geometry)
        child_shape = shape(child_geometry)
        children.append(child_shape)

    #TODO merge child geometries
    geometry = cascaded_union(children)
    mapped_geometry = mapping(geometry)
    #TODO create the region
    #TODO return the region

    return {"geometry": mapped_geometry, "name": name, "type": kind}
