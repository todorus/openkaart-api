import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import tests.lib.utils as utils
import json


class Login(unittest.TestCase):

    # Given I have an admin username and password defined

    # TODO clear database and add an admin user
    # def setUp(self):

    def test_with_correct_credentials(self):

        # When I try to login with this combination
        payload = {"username": "admin", "password": "correct"}
        req = requests.post("http://web/login", data=payload)

        # Then it should return an OK status
        self.assertEquals(200, req.status_code)
        # And a user
        self.assertEquals({"username": "admin"}, req.json)

    def test_incorrect_password(self):

        # When I try to login with an unknown combination
        payload = {"username": "admin", "password": "incorrect"}
        req = requests.post("http://web/login", data=payload)

        # Then it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And an empty body
        self.assertEquals("", req.text)

    def test_incorrect_username(self):

        # When I try to login with an unknown combination
        payload = {"username": "incorrect", "password": "correct"}
        req = requests.post("http://web/login", data=payload)

        # Then it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And an empty body
        self.assertEquals("", req.text)
