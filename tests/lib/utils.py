import app.lib.db.setup as db
import app.lib.model.user as user
import requests
from unittest import TestCase

TestCase.maxDiff = None


def wipe_db(graph):
    graph.data("MATCH (n) OPTIONAL MATCH (n)-[r]->(m) DELETE n,m,r")


def login(graph):
    user_definitions = [
        {u"username": "user1", u"password": u'password1'},
    ]
    user.createAll(graph, user_definitions)

    payload = {"username": "user1", "password": "password1"}
    loginReq = requests.post("http://web/users/login", json=payload)
    token = loginReq.headers["JWT"]
    headers = {"Authorization": "Bearer %s" % token}
    return headers
