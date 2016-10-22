import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import tools.utils as utils
import json


class FetchRegions(unittest.TestCase):

    # Given I have a aset of regions
    # And they are not sorted by name or type

    def setUp(self):
        graph = db.init_graph()
        utils.wipe_db(graph)

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
        region.createAll(graph, definitions)

    def test_without_parameters(self):

        # When I request Regions without parameters
        req = requests.get("http://web/regions")

        # Then it should return all Regions
        # And it should be ordered by name
        # And provide pagination data
        expected = {
          "pages": {
            "current": 1,
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
        self.assertEquals(expected, req.json())

    def test_with_matching_query_ordered_by_length(self):

        # When I request Regions with a query
        # And it matches part of the names of some Regions
        req = requests.get("http://web/regions?q=%s" % ("oss"))

        # Then it should return a list of regions filtered by that query
        # And it should be ordered by length
        # And provide pagination data
        expected = {
          "pages": {
            "current": 1,
            "total": 1
          },
          "data": [
            {"geometry": [[9, 1]], "name": 'Oss', "type": region.PLACE},
            {"geometry": [[8, 1]], "name": 'Ossdam', "type": region.PLACE},
          ]
        }
        self.assertEquals(expected, req.json())

    def test_with_matching_query_ordered_by_name(self):

        # When I request Regions with a query
        # And it matches part of the names of some Regions
        req = requests.get("http://web/regions?q=%s" % ("maas"))

        # Then it should return a list of regions filtered by that query
        # And it should be ordered by length
        # And provide pagination data
        expected = {
          "pages": {
            "current": 1,
            "total": 1
          },
          "data": [
            {"geometry": [[2, 1]], "name": 'Maasdamn', "type": region.PLACE},
            {"geometry": [[6, 1]], "name": 'Maasland', "type": region.MUNICIPALITY},
            {"geometry": [[1, 1]], "name": 'Maastricht', "type": region.PLACE},
          ]
        }
        self.assertEquals(expected, req.json())

    def test_with_non_matching_query(self):

        # When I request Regions with a query
        # And it matches none of the Regions names nor parts of them
        req = requests.get("http://web/regions?q=%s" % ("qii"))

        # Then it should return an empty list
        # And provide pagination data
        expected = {
          "pages": {
            "current": 1,
            "total": 1
          },
          "data": []
        }
        self.assertEquals(expected, req.json())

    def test_pagination_with_only_a_limit(self):

        # When I request Regions
        # And I provide a limit of the amount of results per page
        req = requests.get("http://web/regions?limit=%d" % (2))

        # Then it should return a list of all the Regions
        # And limit them by the specified limit
        # And provide pagination data
        expected = {
          "pages": {
            "current": 1,
            "total": 5
          },
          "data": [
            {"geometry": [[3, 1]], "name": 'bijdeMaas', "type": region.MUNICIPALITY},
            {"geometry": [[10, 1]], "name": 'blib', "type": region.MUNICIPALITY},
          ]
        }
        self.assertEquals(expected, req.json())

    def test_pagination_with_a_limit_and_page(self):

        # When I request Regions
        # And I provide a limit of the amount of results per page
        req = requests.get("http://web/regions?limit=%d&page=%d" % (2, 2))

        # Then it should return a list of all the Regions
        # And limit them by the specified limit
        # And provide pagination data
        expected = {
          "pages": {
            "current": 2,
            "total": 5
          },
          "data": [
            {"geometry": [[5, 1]], "name": 'blob', "type": region.MUNICIPALITY},
            {"geometry": [[4, 1]], "name": 'blub', "type": region.MUNICIPALITY},
          ]
        }
        self.assertEquals(expected, req.json())

    def test_pagination_with_a_limit_and_query(self):

        # When I request Regions
        # And I provide a limit of the amount of results per page
        req = requests.get("http://web/regions?q=%s&limit=%d" % ("maas", 2))

        # Then it should return a list of all the Regions
        # And limit them by the specified limit
        # And provide pagination data
        expected = {
          "pages": {
            "current": 1,
            "total": 2
          },
          "data": [
            {"geometry": [[2, 1]], "name": 'Maasdamn', "type": region.PLACE},
            {"geometry": [[6, 1]], "name": 'Maasland', "type": region.MUNICIPALITY},
          ]
        }
        self.assertEquals(expected, req.json())
