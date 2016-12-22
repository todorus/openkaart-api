import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.user as user
import tests.lib.utils as utils


class Login(unittest.TestCase):

    # Given I have an admin username and password defined
    def setUp(self):
        graph = db.init_graph()
        utils.wipe_db(graph)

        definitions = [
            {u"username": "user1", u"password": u'password1'},
            {u"username": "user2", u"password": u'password2'},
            {u"username": "user3", u"password": u'password3'},
        ]
        user.createAll(graph, definitions)

    def test_with_correct_credentials(self):

        # When I try to login with this combination
        payload = {"username": "user2", "password": "password2"}
        req = requests.post("http://web/users/login", json=payload)

        # Then it should return an OK status
        self.assertEquals(200, req.status_code)
        # And a user
        self.assertEquals({"username": "user2"}, req.json())

    def test_incorrect_password(self):

        # When I try to login with an incorrect password
        payload = {"username": "user1", "password": "incorrect"}
        req = requests.post("http://web/users/login", json=payload)

        # Then it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And an empty body
        self.assertEquals("", req.text)

    def test_incorrect_username(self):

        # When I try to login with an incorrect combination
        payload = {"username": "user3", "password": "password1"}
        req = requests.post("http://web/users/login", json=payload)

        # Then it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And an empty body
        self.assertEquals("", req.text)
