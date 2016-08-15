import json
from app.model import region
from py2neo import Node, Relationship
import py2neo

def printRelation(relationship):
    walkable = py2neo.walk(relationship)
    print "(%s) -[%s]-> (%s)" % (relationship.start_node()["name"], relationship.type(), relationship.end_node()["name"])


def execute(graph, databaseName, fileName):
    data = json.load(open(fileName))
    for item in data:
        provinceName = item["Provincie"]
        municipalityCode = item["Gemeentecode"]
        zipCode = item['Postcode']

        province = region.match(graph, databaseName, {"type": region.PROVINCE, "name": provinceName})
        municipality = region.match(graph, databaseName, {"type": region.MUNICIPALITY, "code": municipalityCode})
        zipArea = region.match(graph, databaseName, {"type": region.ZIP, "code": zipCode})

        if len(province) > 0:
            if len(municipality) > 0:
                existingRelations = graph.match(province[0], None, municipality[0])
                if len(existingRelations == 0):
                    ab = Relationship(province[0], "CONTAINS", municipality[0])
                    graph.create(ab)
                    printRelation(ab)
            elif len(zipArea) > 0:
                ab = Relationship(province[0], "CONTAINS", zipArea[0])
                graph.create(ab)
                printRelation(ab)

        if len(municipality) > 0 and len(zipArea) > 0:
            ab = Relationship(municipality[0], "CONTAINS", zipArea[0])
            graph.create(ab)
            printRelation(ab)
