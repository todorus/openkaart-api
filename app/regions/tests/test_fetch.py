import unittest
import app.fetch.handler as handler
import app.lib.db.setup as db
import app.lib.model.region as region
import utils
import json

graph = db.init_graph("test")
databaseName = "test_database"


class FetchRegions(unittest.TestCase):

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

    def without_parameters(self):
        event = {
            "query": "nij"
        }
        result = handler.handler(event, None)

        expected = {
          "pages": {
            "current": 0,
            "total": 1
          },
          "data": [
            {"geometry": [[3, 1]], "name": 'bijdeMaas', "type": region.MUNICIPALITY},
            {"geometry": [[10, 1]], "name": 'blib', "type": region.MUNICIPALITY},
            {"geometry": [[5, 1]], "name": 'blob', "type": region.MUNICIPALITY},
            {"geometry": [[4, 1]], "name": 'blub', "type": region.MUNICIPALITY},
            {"geometry": [[2, 1]], "name": 'Maasdamn', "type": region.PLACE},
            {"geometry": [[6, 1]], "name": 'Maasland', "type": region.MUNICIPALITY},
            {"geometry": [[1, 1]], "name": 'Maastricht', "type": region.PLACE},
            {"geometry": [[9, 1]], "name": 'Oss', "type": region.PLACE},
            {"geometry": [[8, 1]], "name": 'Ossdam', "type": region.PLACE},
            {"geometry": [[7, 1]], "name": 'Overblaak', "type": region.PLACE},
          ]
        }

        # self.assertEquals(json.loads(result), expected)
        self.assertEquals(json.loads(json.dumps(result)), json.loads(json.dumps(expected)))
