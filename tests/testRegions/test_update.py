import unittest
import logging
import requests
import collections
import app.lib.db.setup as db
import app.lib.model.region as region
import app.lib.model.relations as relations
import tests.lib.utils as utils
from py2neo import Relationship


class UpdateRegion(unittest.TestCase):

    # Given I have a a set of regions

    def setUp(self):
        self.graph = db.init_graph()
        utils.wipe_db(self.graph)

        # testdata from http://turfjs.org/static/docs/module-turf_merge.html

        self.polyA = {
            u"type": u"Polygon",
            u"coordinates": [
              [
                [
                  9.994812,
                  53.549487
                ],
                [
                  10.046997,
                  53.598209
                ],
                [
                  10.117721,
                  53.531737
                ],
                [
                  9.994812,
                  53.549487
                ]
              ]
            ]
        }

        self.polyB = {
            u"type": u"Polygon",
            u"coordinates": [
              [
                [
                  10.000991,
                  53.50418
                ],
                [
                  10.03807,
                  53.562539
                ],
                [
                  9.926834,
                  53.551731
                ],
                [
                  10.000991,
                  53.50418
                ]
              ]
            ]
        }

        self.polyAB = {
            u"type": u"Polygon",
            u"coordinates": [
                [
                    [10.026838636912657, 53.54486184801601],
                    [10.000991, 53.50418],
                    [9.926834, 53.551731],
                    [10.005390809136088, 53.55936379867258],
                    [10.046997, 53.598209],
                    [10.117721, 53.531737],
                    [10.026838636912657, 53.54486184801601]
                ]
            ]
        }

        region_definitions = [
            {u"geometry": self.polyA, u"name": u'1001', u"type": region.ZIP, u"uuid": u"1"},
            {u"geometry": self.polyB, u"name": u'1002', u"type": region.ZIP, u"uuid": u"2"},
            {u"geometry": self.polyAB, u"name": u'Maas', u"type": region.MUNICIPALITY, u"uuid": u"3"},
            {u"geometry": self.polyA, u"name": u'Subject', u"type": region.CARE, u"uuid": u"4"}
        ]
        region.createAll(self.graph, region_definitions)
        self.regionCount = region.count(self.graph)

        region0 = region.find(self.graph, region_definitions[0])
        region1 = region.find(self.graph, region_definitions[1])
        region2 = region.find(self.graph, region_definitions[2])
        region3 = region.find(self.graph, region_definitions[3])
        self.graph.create(Relationship(region0, relations.BELONGS_TO, region2))
        self.graph.create(Relationship(region0, relations.BELONGS_TO, region3))
        self.graph.create(Relationship(region1, relations.BELONGS_TO, region2))

        self.subject_definition = region_definitions[3]


    def test_update_unauthorized(self):
        # And I NOT logged in
        # When I update a Region
        payload = {
            "name": "new_name"
        }
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload)

        # Then it should return an UNAUTHORIZED status

        self.assertEquals(401, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And the Region should not be updated
        #TODO check if it has not changed

    def test_update_without_properties(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Region without specifying children
        payload = {}
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And the Region should not be updated
        #TODO check if it has not changed


    def test_invalid_name(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I update a Region by specifying an invalid name
        payload = {
            "name": ""
        }
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And the Region should not be updated
        #TODO check if it has not changed

    def test_invalid_type(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I update a Region by specifying an invalid name
        payload = {
            "type": ""
        }
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And the Region should not be updated
        #TODO check if it has not changed

    def test_unknown_child(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I update a new Region from several Regions
        payload = {
            "children": [u"2", u"-1"]
        }
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload, headers=headers)

        # Then it should return an NOT FOUND status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And the Region should not be updated
        #TODO check if it has not changed

    def test_change_children(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I update a Region, by chaning its children
        payload = {
            "children": [u"2", u"1"]
        }
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload, headers=headers)

        # Then it should return an OK status

        self.assertEquals(200, req.status_code)

        # And the newly updated Region
        expected = self.subject_definition
        expected["geometry"] = self.polyAB

        response_json = req.json()
        self.assertEquals(expected, response_json)

        # And the Region has the correct children
        updated_region = region.find(self.graph, {"uuid": uuid})
        children, childCount = region.children(self.graph, updated_region["uuid"])
        self.assertEquals(2, childCount)
        #TODO check if it are the correct children

    def test_change_name(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I update a Region by specifying an invalid name
        payload = {
            "name": "new_name"
        }
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload, headers=headers)

        # Then it should return an OK status

        self.assertEquals(200, req.status_code)

        # And the newly updated Region
        expected = self.subject_definition
        expected["name"] = payload["name"]

        response_json = req.json()
        response_json = req.json()
        self.assertEquals(expected["uuid"], response_json["uuid"])
        self.assertEquals(expected["name"], response_json["name"])
        self.assertEquals(expected["type"], response_json["type"])
        self.assertEquals(self.polyA, response_json["geometry"])

        # And the Region is updated
        #TODO check if region is updated

    def test_change_type(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I update a Region by specifying an invalid name
        payload = {
            "type": region.MUNICIPALITY
        }
        uuid = u"4"
        url = "http://web/regions/%s" % uuid
        req = requests.put(url, json=payload, headers=headers)

        # Then it should return an OK status

        self.assertEquals(200, req.status_code)

        # And the newly updated Region
        expected = self.subject_definition
        expected["type"] = payload["type"]

        response_json = req.json()
        self.assertEquals(expected["uuid"], response_json["uuid"])
        self.assertEquals(expected["name"], response_json["name"])
        self.assertEquals(expected["type"], response_json["type"])
        self.assertEquals(self.polyA, response_json["geometry"])

        # And the Region is updated
        #TODO check if region is updated

    def assertDictEqual(self, d1, d2, msg=None): # assertEqual uses for dicts
        for k,v1 in d1.iteritems():
            self.assertIn(k, d2, msg)
            v2 = d2[k]
            if(isinstance(v1, collections.Iterable) and
               not isinstance(v1, basestring)):
                self.assertItemsEqual(v1, v2, msg)
            else:
                self.assertEqual(v1, v2, msg)
        return True
