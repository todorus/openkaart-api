import json
import geojson
from shapely.geometry import shape
from scraper import FileScraper, WFSScraper


class MunicipalityFileScraper(FileScraper):
    def __init__(self, basePath):
        super(MunicipalityFileScraper, self).__init__(basePath)

    def write(self, json_string, page):
        writeToDb(self.conn, self.cur, json_string)


class MunicipalityWFSScraper(WFSScraper):

    def writeToDb(self, json_string):
        writeToDb(self.conn, self.cur, json_string)


def writeToDb(connection, cursor, json_string):
    data = json.loads(json_string)
    features = data["features"]
    for feature in features:
        properties = feature["properties"]
        code = int(properties["statcode"][2:])
        name = properties["statnaam"]

        geometry_dump = json.dumps(feature["geometry"])
        geometry_geojson = geojson.loads(geometry_dump)
        geometry_wkt = shape(geometry_geojson).wkt

        data = (code, name, geometry_wkt)

        cursor.execute("INSERT INTO municipalities (code, name, geometry) VALUES (%s, %s, ST_GeomFromText(%s))", data)
        print "inserted municipality %s, %s" % (code, name)
    connection.commit()
