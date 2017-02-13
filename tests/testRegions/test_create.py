import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import app.lib.model.user as user
import app.lib.model.relations as relations
import tests.lib.utils as utils
from py2neo import Relationship


class CreateRegion(unittest.TestCase):

    # Given I have a a set of regions

    def setUp(self):
        self.graph = db.init_graph()
        utils.wipe_db(self.graph)

        # testdata from http://turfjs.org/static/docs/module-turf_merge.html

        self.polyA = {
            "type": "Polygon",
            "coordinates": [
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
            "type": "Polygon",
            "coordinates": [
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
            {u"geometry": self.polyAB, u"name": u'Maas', u"type": region.MUNICIPALITY, u"uuid": u"3"}
        ]
        region.createAll(self.graph, region_definitions)
        self.regionCount = region.count(self.graph)

        region0 = region.find(self.graph, region_definitions[0])
        region1 = region.find(self.graph, region_definitions[1])
        region2 = region.find(self.graph, region_definitions[2])
        self.graph.create(Relationship(region0, relations.BELONGS_TO, region2))
        self.graph.create(Relationship(region1, relations.BELONGS_TO, region2))


    def test_create_unauthorized(self):
        # And I NOT logged in
        # When I create a new Region from several Regions
        payload = {
            "name": "new_region",
            "type": "Care",
            "children": [u"1", u"2"]
        }
        url = "http://web/regions"
        req = requests.post(url, json=payload)

        # Then it should return an UNAUTHORIZED status

        self.assertEquals(401, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been a Region created
        self.assertEquals(self.regionCount, region.count(self.graph))

    def test_without_children(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Region without specifying children
        payload = {
            "name": "new_region",
            "type": "Care",
            "children": []
        }
        url = "http://web/regions"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been a Region created
        self.assertEquals(self.regionCount, region.count(self.graph))

    def test_without_name(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Region without specifying a name
        payload = {
            "type": "Care",
            "children": [u"1", u"2"]
        }
        url = "http://web/regions"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been a Region created
        self.assertEquals(self.regionCount, region.count(self.graph))

    def test_invalid_name(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Region without specifying a name
        payload = {
            "name": "",
            "type": "Care",
            "children": [u"1", u"2"]
        }
        url = "http://web/regions"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an 400 status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been a Region created
        self.assertEquals(self.regionCount, region.count(self.graph))

    def test_unknown_child(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Region from several Regions
        uuid = u"1"
        payload = {
            "name": "new_region",
            "type": "Care",
            "children": [u"2", u"-1"]
        }
        url = "http://web/regions"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an NOT FOUND status
        self.assertEquals(400, req.status_code)

        # And an empty body
        self.assertEquals("", req.text)

        # And there should not have been a Region created
        self.assertEquals(self.regionCount, region.count(self.graph))

    def test_create_from_multiple(self):
        # And I am logged in
        headers = utils.login(self.graph)

        # When I create a new Region from several Regions
        uuid = u"1"
        payload = {
            "name": "new_region",
            "type": "Care",
            "children": [u"2", u"1"]
        }
        url = "http://web/regions"
        req = requests.post(url, json=payload, headers=headers)

        # Then it should return an OK status

        self.assertEquals(200, req.status_code)

        # And the newly created Region
        response_json = req.json()
        if "uuid" in response_json:
            response_json.pop("uuid")
        expected = {
            u"geometry": self.polyAB,
            u"name": u"new_region",
            u"type": u"Care"
        }
        self.assertEquals(expected, response_json)

        # And the Region is created
        self.assertEquals(self.regionCount + 1, region.count(self.graph))
        # And the Region has the correct children
        new_region = region.find(self.graph, {"uuid": req.json()["uuid"]})
        children, childCount = region.children(self.graph, new_region["uuid"])
        self.assertEquals(2, childCount)
        print(children)
