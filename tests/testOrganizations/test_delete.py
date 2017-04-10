import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.organization as organizations
import tests.lib.utils as utils


class DeleteOrganization(unittest.TestCase):

    # Given I have a set of Organizations

    def setUp(self):
        self.graph = db.init_graph()
        utils.wipe_db(self.graph)

        self.definitions = [
            {u"uuid": u'uuid1', u"name": u'Eurocorp', u"phone": u'1234', u"email": u'info@euro.corp', u"address": u'Brussels'},
            {u"uuid": u'uuid2',u"name": u'Church of the New Epoch', u"phone": u'5678', u"email": u'info@epoch.js', u"address": u'Up'}
        ]
        organizations.createAll(self.graph, self.definitions)

    def test_success(self):
        # And I am logged in
        headers = utils.login(self.graph)
        # And specific one is in the database
        uuid = self.definitions[0][u"uuid"]
        self.assertTrue(organizations.exists(self.graph, {"uuid": uuid}))

        # When I delete an Organization by uuid
        url = "http://web/organizations/%s" % (uuid)
        req = requests.delete(url, headers=headers)

        # Then the Organization removed from the database
        self.assertFalse(organizations.exists(self.graph, {"uuid": uuid}))
        # And it should return an OK status
        self.assertEquals(200, req.status_code)
        # And the body is empty
        self.assertEquals("", req.text)
        # And its Locations are removed
        # FIXME write tests for deleting locations as well

    def test_404(self):
        count = organizations.count(self.graph)

        # And I am logged in
        headers = utils.login(self.graph)

        # When I request an Organization by uuid
        # And there is no Organization by that uuid
        uuid = "non-existant"
        url = "http://web/organizations/%s" % (uuid)
        req = requests.delete(url, headers=headers)

        # Then no Organization should be deleted
        self.assertEquals(count, organizations.count(self.graph))
        # And it should return a NOT FOUND status
        self.assertEquals(404, req.status_code)
        # And the body is empty
        self.assertEquals("", req.text)

    def test_not_logged_in(self):
        count = organizations.count(self.graph)

        # And I am not logged in
        headers = None

        # When I request an Organization by uuid
        # And there is no Organization by that uuid
        uuid = "non-existant"
        url = "http://web/organizations/%s" % (uuid)
        req = requests.delete(url, headers=headers)

        # Then no Organization should be deleted
        self.assertEquals(count, organizations.count(self.graph))
        # And it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And the body is empty
        self.assertEquals("", req.text)
