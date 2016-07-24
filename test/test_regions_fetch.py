import unittest
import app.regions.regions_fetch.handler as handler


class RegionsFetchTest(unittest.TestCase):

    event = {
        "query": "nij"
    }

    def test_hello_world(self):
        result = handler.handler(self.event, None)

        expected = {
            "query": "nij"
        }

        self.assertEquals(result, expected)
