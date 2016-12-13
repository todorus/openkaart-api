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

    def test_me_logged_in(self):

        # And I am logged in
        payload = {"username": "user2", "password": "password2"}
        loginReq = requests.post("http://web/login", json=payload)

        # When I ask for my user
        req = requests.get("http://web/me", cookies=loginReq.cookies)

        # Then it should return a NOT FOUND status
        self.assertEquals(200, req.status_code)
        # And a user
        self.assertEquals({"username": "user2"}, req.json())

    def test_me_not_logged_in(self):

        # And I am not logged in

        # When I ask for my user
        req = requests.get("http://web/me")

        # Then it should return an NOT FOUND status
        self.assertEquals(401, req.status_code)
        # And an empty body
        self.assertEquals("", req.text)
