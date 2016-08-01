import unittest
import app.regions.regions_fetch.handler as handler
import app.db.setup as db
import app.model.region as region
import utils

graph = db.init_graph("test")
databaseName = "test_database"


class RegionsFetchTest(unittest.TestCase):

    event = {
        "query": "nij"
    }

    def setUp(self):
        utils.wipe_db(graph, databaseName)

        definitions = [
            {"geometry": [[1, 1]], "name": 'Maastricht', "type": region.PLACE},
            {"geometry": [[2, 1]], "name": 'Maasdamn', "type": region.PLACE},
            {"geometry": [[3, 1]], "name": 'bijdeMaas', "type": region.MUNICIPALITY},
            {"geometry": [[4, 1]], "name": 'blub', "type": region.MUNICIPALITY},
            {"geometry": [[5, 1]], "name": 'blob', "type": region.MUNICIPALITY},
            {"geometry": [[6, 1]], "name": 'Maasland', "type": region.MUNICIPALITY},
            {"geometry": [[7, 1]], "name": 'Overblaak', "type": region.PLACE},
            {"geometry": [[8, 1]], "name": 'Ossdam', "type": region.PLACE},
            {"geometry": [[9, 1]], "name": 'Oss', "type": region.PLACE},
            {"geometry": [[10, 1]], "name": 'blib', "type": region.MUNICIPALITY}
        ]
        region.createAll(graph, databaseName, definitions)

    def test_hello_world(self):
        result = handler.handler(self.event, None)

        expected = {
            "query": "nij"
        }

        self.assertEquals(result, expected)
