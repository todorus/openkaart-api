import json
import geojson
import psycopg2
from shapely.geometry import shape

conn = psycopg2.connect("dbname=openkaart_development user=todorus")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS postalcodes_to_municipalities")
cur.execute('CREATE TABLE postalcodes_to_municipalities (id serial PRIMARY KEY, municipality_id integer, postalcode_id integer, UNIQUE (municipality_id, postalcode_id))')

data = json.load(open("adressen.geo.json"))
features = data["features"]
for feature in features:
    properties = feature["properties"]

    geometry_dump = json.dumps(feature["geometry"])
    geometry_geojson = geojson.loads(geometry_dump)
    geometry_wkt = shape(geometry_geojson).wkt

    print properties

    cur.execute("""
    INSERT INTO postalcodes_to_municipalities (municipality_id, postalcode_id)
    SELECT municipalities.id, postal_codes.id
    FROM municipalities, postal_codes
    WHERE ST_CONTAINS(municipalities.geometry, ST_GeomFromText(%s))
    AND postal_codes.name = %s
    ON CONFLICT DO NOTHING
    """, (geometry_wkt, properties["postcode"][0:4]))

conn.commit()

cur.close()
conn.close()
