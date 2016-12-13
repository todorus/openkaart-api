import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.user as user
import tests.lib.utils as utils


class Login(unittest.TestCase):

    def setUp(self):
        # Given I have an admin username and password defined
        graph = db.init_graph()
        utils.wipe_db(graph)

        definitions = [
            {u"username": "user1", u"password": u'password1'},
            {u"username": "user2", u"password": u'password2'},
            {u"username": "user3", u"password": u'password3'},
        ]
        user.createAll(graph, definitions)

    def test_view_current_user(self):

        # And I am logged in
        payload = {"username": "user2", "password": "password2"}
        req = requests.post("http://web/login", json=payload)

        # When I ask for the current logged in user

        # Then it should return an OK status
        self.assertEquals(200, req.status_code)
        # And a user
        self.assertEquals({"username": "user2"}, req.json())
