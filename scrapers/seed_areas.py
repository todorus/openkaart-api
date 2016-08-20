import json
import geojson
import string
import psycopg2
from shapely.geometry import shape

regions_table_name = "regions"

conn = psycopg2.connect("dbname=openkaart_development user=todorus")
cur = conn.cursor()


print "municipalities"
cur.execute("DROP TABLE IF EXISTS municipalities")
cur.execute('CREATE TABLE municipalities (id serial PRIMARY KEY, code integer, name varchar, "geometry" geometry)')

data = json.load(open("municipalities.geo.json"))
features = data["features"]
for feature in features:
    properties = feature["properties"]
    code = int(properties["statcode"][2:])
    name = properties["statnaam"]

    geometry_dump = json.dumps(feature["geometry"])
    geometry_geojson = geojson.loads(geometry_dump)
    geometry_wkt = shape(geometry_geojson).wkt

    data = (code, name, geometry_wkt)

    cur.execute("INSERT INTO municipalities (code, name, geometry) VALUES (%s, %s, ST_GeomFromText(%s))", data)
    print "inserted municipality %s, %s" % (code, name)
conn.commit()

print "postal codes"
cur.execute("DROP TABLE IF EXISTS postal_codes")
cur.execute("CREATE TABLE postal_codes (id serial PRIMARY KEY, name varchar)")

for number in range(0,10000):
    name = str(number).zfill(4)
    data = (name,)
    cur.execute("INSERT INTO postal_codes (name) VALUES (%s)", data)
    print "inserted postal area %s" % (name)
conn.commit()


cur.close()
conn.close()
