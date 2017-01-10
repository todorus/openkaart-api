import unittest
import requests
import time
import app.lib.db.setup as db
import app.lib.model.user as user
import app.lib.jwt as jwt
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
            {u"username": "user4", u"password": u'password4', u"uuid": u'uuid4'},
        ]
        user.createAll(graph, definitions)

    def test_me_logged_in(self):

        # And I am logged in
        payload = {"username": "user2", "password": "password2"}
        loginReq = requests.post("http://web/users/login", json=payload)
        token = loginReq.headers["JWT"]

        # When I ask for my user
        headers = {"Authorization": "Bearer %s" % token}
        req = requests.get("http://web/users/me", headers=headers)

        # Then it should return an OK status
        self.assertEquals(200, req.status_code)
        # And a user
        self.assertEquals({"username": "user2"}, req.json())
        # And a fresh JWT token
        assert "JWT" in req.headers
        # TODO check token correctness

    def test_me_not_logged_in(self):

        # And I am not logged in

        # When I ask for my user
        req = requests.get("http://web/users/me")

        # Then it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And an empty body
        self.assertEquals("", req.text)

    def test_expired_token(self):
        # And I am logged in, with an expired token
        exp = time.time() - 20
        iat = exp - 1000

        token_data = {
            "sub": u'uuid4'
        }
        token = jwt.encode(token_data, iat=iat, exp=exp)

        # When I ask for my user
        headers = {"Authorization": "Bearer %s" % token}
        req = requests.get("http://web/users/me", headers=headers)

        # Then it should return an UNAUTHORIZED status
        self.assertEquals(401, req.status_code)
        # And an empty body
        self.assertEquals("", req.text)

    def test_valid_token(self):
        # And I am logged in, with a valid token
        iat = time.time() - 10
        exp = iat + 100000

        token_data = {
            "sub": u'uuid4'
        }
        token = jwt.encode(token_data, iat=iat, exp=exp)

        # When I ask for my user
        headers = {"Authorization": "Bearer %s" % token}
        req = requests.get("http://web/users/me", headers=headers)

        # Then it should return an OK status
        self.assertEquals(200, req.status_code)
        # And a user
        self.assertEquals({"username": "user4"}, req.json())
