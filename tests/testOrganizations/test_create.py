import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import app.lib.model.organization as organization
import app.lib.model.relations as relations
import tests.lib.utils as utils
from py2neo import Relationship


class CreateOrganization(unittest.TestCase):

    # Given I have a a set of regions

    def setUp(self):
        self.graph = db.init_graph()
        utils.wipe_db(self.graph)

        region_definitions = [
            {u"geometry": [[1, 1]], u"name": u'Maastricht', u"type": region.PLACE, u"uuid": "1"},
            {u"geometry": [[2, 1]], u"name": u'Maasdamn', u"type": region.PLACE, u"uuid": "2"},
            {u"geometry": [[3, 1]], u"name": u'bijdeMaas', u"type": region.MUNICIPALITY, u"uuid": "3"},
            {u"geometry": [[4, 1]], u"name": u'blub', u"type": region.MUNICIPALITY, u"uuid": "4"},
            {u"geometry": [[5, 1]], u"name": u'blob', u"type": region.MUNICIPALITY, u"uuid": "5"},
            {u"geometry": [[6, 1]], u"name": u'Maasland', u"type": region.MUNICIPALITY, u"uuid": "6"},
            {u"geometry": [[7, 1]], u"name": u'Overblaak', u"type": region.PLACE, u"uuid": "7"},
            {u"geometry": [[8, 1]], u"name": u'Ossdam', u"type": region.PLACE, u"uuid": "8"},
            {u"geometry": [[9, 1]], u"name": u'Oss', u"type": region.PLACE, u"uuid": "9"},
            {u"geometry": [[10, 1]], u"name": u'blib', u"type": region.MUNICIPALITY, u"uuid": "10"}
        ]
        region.createAll(self.graph, region_definitions)

        self.organizationCount = organization.count(self.graph)


    def test_create_unauthorized(self):
        # And I NOT logged in
        # When I create a new Organization
        payload = {
            "name": "new_organization",
            "contact_data": {
                "phone": "1234567890",
                "email": "some@email.com",
                "address": "That street 17",
            }
        }
        url = "http://web/organizations"
        req = requests.post(url, json=payload)

        # Then it should return an UNAUTHORIZED status

        self.assertEquals(401, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been an Organization created
        self.assertEquals(self.organizationCount, organization.count(self.graph))

    def test_without_name(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Organization without specifying its name
        payload = {
            "contact_data": {
                "phone": "1234567890",
                "email": "some@email.com",
                "address": "That street 17",
            }
        }
        url = "http://web/organizations"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been an Organization created
        self.assertEquals(self.organizationCount, organization.count(self.graph))

    def test_invalid_name(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Organization without specifying a name
        payload = {
            "name": "",
            "contact_data": {
                "phone": "1234567890",
                "email": "some@email.com",
                "address": "That street 17",
            }
        }
        url = "http://web/organizations"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been an Organization created
        self.assertEquals(self.organizationCount, organization.count(self.graph))

    def test_create_valid(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Organization with valid data
        payload = {
            "name": "new_organization",
            "contact_data": {
                "phone": "1234567890",
                "email": "some@email.com",
                "address": "That street 17",
            }
        }
        url = "http://web/organizations"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an OK status

        self.assertEquals(200, req.status_code)

        # And the newly created Organization
        response_json = req.json()
        if "uuid" in response_json:
            response_json.pop("uuid")
        expected = {
            u"name": u"new_organization",
            u"contact_data": {
                u"phone": u"1234567890",
                u"email": u"some@email.com",
                u"address": u"That street 17",
            }
        }
        self.assertEquals(expected, response_json)

        # And the Organization is created
        self.assertEquals(self.organizationCount + 1, organization.count(self.graph))
