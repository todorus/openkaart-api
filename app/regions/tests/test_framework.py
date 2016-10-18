import unittest
import requests
import app.lib.db.setup as db
import app.lib.model.region as region
import tools as utils


class FetchRegions(unittest.TestCase):

    def test_hello_world(self):
        print "getting"
        req = requests.get("http://api:5000/fetch")
        self.assertEquals("Hello Fetch!", req.text)
