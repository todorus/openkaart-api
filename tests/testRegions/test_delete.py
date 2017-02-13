import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import tests.lib.utils as utils


class DeleteRegion(unittest.TestCase):

    # Given I have a aset of regions

    def setUp(self):
        self.graph = db.init_graph()
        utils.wipe_db(self.graph)

        self.definitions = [
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
        region.createAll(self.graph, self.definitions)

    def test_success(self):
        # And I am logged in
        headers = utils.login(self.graph)
        # And specific one is in the database
        uuid = self.definitions[0][u"uuid"]
        self.assertTrue(region.exists(self.graph, {"uuid": uuid}))

        # When I delete a region by uuid
        url = "http://web/regions/%s" % (uuid)
        req = requests.delete(url, headers=headers)

        # Then the Region removed from the database
        self.assertFalse(region.exists(self.graph, {"uuid": uuid}))
        # And it should return an OK status
        self.assertEquals(200, req.status_code)
        # And the body is empty
        self.assertEquals("", req.text)

    def test_404(self):
        count = region.count(self.graph)

        # And I am logged in
        headers = utils.login(self.graph)

        # When I request a Region by uuid
        # And there is no Region by that uuid
        uuid = "non-existant"
        url = "http://web/regions/%s" % (uuid)
        req = requests.delete(url, headers=headers)

        # Then no Region should be deleted
        self.assertEquals(count, region.count(self.graph))
        # And it should return a NOT FOUND status
        self.assertEquals(404, req.status_code)
        # And the body is empty
        self.assertEquals("", req.text)

    def test_not_logged_in(self):
        count = region.count(self.graph)

        # And I am not logged in
        headers = None

        # When I request a Region by uuid
        # And there is no Region by that uuid
        uuid = "non-existant"
        url = "http://web/regions/%s" % (uuid)
        req = requests.delete(url, headers=headers)

        # Then no Region should be deleted
        self.assertEquals(count, region.count(self.graph))
        # And it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And the body is empty
        self.assertEquals("", req.text)
