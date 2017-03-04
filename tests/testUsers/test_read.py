import unittest
import requests
import time
import app.lib.db.setup as db
import app.lib.model.user as user
import app.lib.jwt as jwt
import tests.lib.utils as utils
import base64
import json


class Login(unittest.TestCase):

    # Given I have an admin username and password defined
    def setUp(self):
        graph = db.init_graph()
        utils.wipe_db(graph)

        self.definitions = [
            {u"username": "user1", u"password": u'password1', u"uuid": u'uuid1'},
            {u"username": "user2", u"password": u'password2', u"uuid": u'uuid2'},
            {u"username": "user3", u"password": u'password3', u"uuid": u'uuid3'},
            {u"username": "user4", u"password": u'password4', u"uuid": u'uuid4'},
        ]
        user.createAll(graph, self.definitions)

    # def test_me_logged_in(self):
    #
    #     # And I am logged in
    #     payload = {"username": "user2", "password": "password2"}
    #     loginReq = requests.post("http://web/users/login", json=payload)
    #     token = loginReq.headers["JWT"]
    #
    #     # When I ask for my user
    #     headers = {"Authorization": "Bearer %s" % token}
    #     req = requests.get("http://web/users/me", headers=headers)
    #
    #     # Then it should return an OK status
    #     self.assertEquals(200, req.status_code)
    #     # And a user
    #     self.assertEquals({"username": "user2"}, req.json())
    #     # And a fresh JWT token
    #     assert "JWT" in req.headers
    #     payload_encoded = req.headers["JWT"].split(".")[1]
    #     payload_encoded = payload_encoded + '=' * (-len(payload_encoded) % 4)
    #     payload_decoded = base64.b64decode(payload_encoded)
    #     payload = json.loads(payload_decoded)
    #     userDef = self.definitions[1] #user2
    #     expected = {
    #         "uuid": userDef[u"uuid"],
    #         "username": userDef[u"username"]
    #     }
    #     self.assertEquals(expected, payload["data"]["sub"])
    #
    # def test_me_not_logged_in(self):
    #
    #     # And I am not logged in
    #
    #     # When I ask for my user
    #     req = requests.get("http://web/users/me")
    #
    #     # Then it should return an UNAUTHORIZED status
    #     self.assertEquals(401, req.status_code)
    #     # And an empty body
    #     self.assertEquals("", req.text)
    #
    # def test_expired_token(self):
    #     # And I am logged in, with an expired token
    #     exp = time.time() - 20
    #     iat = exp - 1000
    #
    #     token_data = {
    #         "sub": u'uuid4'
    #     }
    #     token = jwt.encode(token_data, iat=iat, exp=exp)
    #
    #     # When I ask for my user
    #     headers = {"Authorization": "Bearer %s" % token}
    #     req = requests.get("http://web/users/me", headers=headers)
    #
    #     # Then it should return an UNAUTHORIZED status
    #     self.assertEquals(401, req.status_code)
    #     # And an empty body
    #     self.assertEquals("", req.text)
    #
    # def test_valid_token(self):
    #     # And I am logged in, with a valid token
    #     iat = time.time() - 10
    #     exp = iat + 100000
    #
    #     userDef = self.definitions[3] #user4
    #     token_data = {
    #         "sub": {
    #             "uuid": userDef[u"uuid"],
    #             "username": userDef[u"username"]
    #         }
    #     }
    #     token = jwt.encode(token_data, iat=iat, exp=exp)
    #
    #     # When I ask for my user
    #     headers = {"Authorization": "Bearer %s" % token}
    #     req = requests.get("http://web/users/me", headers=headers)
    #
    #     # Then it should return an OK status
    #     self.assertEquals(200, req.status_code)
    #     # And a user
    #     self.assertEquals({"username": "user4"}, req.json())
