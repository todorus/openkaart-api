import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import app.lib.model.user as user
import tests.lib.utils as utils


class CreateRegion(unittest.TestCase):

    # Given I have a a set of regions

    def setUp(self):
        graph = db.init_graph()
        utils.wipe_db(graph)

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
            "type": "Polygon",
            "coordinates": [
              [
                [
                  10.005390809136088,
                  53.55936379867258
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
                  10.026838636912657,
                  53.54486184801601
                ],
                [
                  10.000991,
                  53.50418
                ],
                [
                  9.926834,
                  53.551731
                ],
                [
                  10.005390809136088,
                  53.55936379867258
                ]
              ]
            ]
        }

        region_definitions = [
            {u"geometry": self.polyA, u"name": u'1001', u"type": region.ZIP, u"uuid": u"1"},
            {u"geometry": self.polyB, u"name": u'1002', u"type": region.ZIP, u"uuid": u"2"},
            {u"geometry": self.polyAB, u"name": u'Maas', u"type": region.MUNICIPALITY, u"uuid": u"3"}
        ]
        region.createAll(graph, region_definitions)

        #TODO create relations

        user_definitions = [
            {u"username": "user1", u"password": u'password1', u"uuid": u'uuid1'},
        ]
        user.createAll(graph, user_definitions)

    def login(self):
        payload = {"username": "user1", "password": "password1"}
        loginReq = requests.post("http://web/users/login", json=payload)
        token = loginReq.headers["JWT"]
        headers = {"Authorization": "Bearer %s" % token}
        return headers

    def test_create_from_multiple(self):
        # And I am logged in
        headers = self.login()

        # When I create a new Region from several Regions
        uuid = u"1"
        payload = {
            "name": "new_region",
            "type": "Care",
            "children": [u"1", u"2"]
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
            u"geometry": polyAB,
            "name": "new_region",
            "type": "Care"
        }
        self.assertEquals(expected, response_json)

        # And the Region is created
        #TODO check
        # And the Region has the correct children
        #TODO check

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
        #TODO check

    def test_without_children(self):
        # And I am logged in
        headers = self.login()

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
        #TODO check

    def test_without_name(self):
        # And I am logged in
        headers = self.login()

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
        #TODO check

    def test_invalid_name(self):
        # And I am logged in
        headers = self.login()

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
        #TODO check
