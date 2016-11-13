import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import tests.lib.utils as utils
import json


class FetchRegions(unittest.TestCase):

    # Given I have a aset of regions
    # And they are not sorted by name or type

    def setUp(self):
        graph = db.init_graph()
        utils.wipe_db(graph)

        definitions = [
            {u"geometry": [[1, 1]], u"name": u'Maastricht', u"type": region.PLACE, u"uuid": u"1"},
            {u"geometry": [[2, 1]], u"name": u'Maasdamn', u"type": region.PLACE, u"uuid": u"2"},
            {u"geometry": [[3, 1]], u"name": u'bijdeMaas', u"type": region.MUNICIPALITY, u"uuid": u"3"},
            {u"geometry": [[4, 1]], u"name": u'blub', u"type": region.MUNICIPALITY, u"uuid": u"4"},
            {u"geometry": [[5, 1]], u"name": u'blob', u"type": region.MUNICIPALITY, u"uuid": u"5"},
            {u"geometry": [[6, 1]], u"name": u'Maasland', u"type": region.MUNICIPALITY, u"uuid": u"6"},
            {u"geometry": [[7, 1]], u"name": u'Overblaak', u"type": region.PLACE, u"uuid": u"7"},
            {u"geometry": [[8, 1]], u"name": u'Ossdam', u"type": region.PLACE, u"uuid": u"8"},
            {u"geometry": [[9, 1]], u"name": u'Oss', u"type": region.PLACE, u"uuid": u"9"},
            {u"geometry": [[10, 1]], u"name": u'blib', u"type": region.MUNICIPALITY, u"uuid": u"10"}
        ]
        region.createAll(graph, definitions)

    def test_read_a(self):

        # When I request a Region by uuid
        uuid = "3"
        url = "http://web/regions/%s" % (uuid)
        req = requests.get(url)

        # Then it should return just the Region
        expected = {u"geometry": [[3, 1]], u"name": u'bijdeMaas', u"type": region.MUNICIPALITY, u"uuid": u"3"}

        self.assertEquals(200, req.status_code)
        self.assertEquals(expected, req.json())

    def test_read_b(self):

        # When I request a Region by uuid
        uuid = "7"
        url = "http://web/regions/%s" % (uuid)
        req = requests.get(url)

        # Then it should return just the Region
        expected = {u"geometry": [[7, 1]], u"name": u'Overblaak', u"type": region.PLACE, u"uuid": u"7"}

        self.assertEquals(200, req.status_code)
        self.assertEquals(expected, req.json())

    def test_read_404(self):
        # When I request a Region by uuid
        # And there is no Region by that uuid
        uuid = "non-existant"
        url = "http://web/regions/%s" % (uuid)
        req = requests.get(url)

        # Then it should return a 404
        self.assertEquals(404, req.status_code)
        # And the body is empty
        self.assertEquals("", req.text)
