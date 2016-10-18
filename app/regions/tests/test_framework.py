import unittest
import app.lib.db.setup as db
import app.lib.model.region as region
import tools as utils
from selenium import webdriver


class FetchRegions(unittest.TestCase):

    def setUp(self):
        print "going"
        self.driver = webdriver.Firefox()
        self.driver.manage().timeouts().implicitlyWait(4, TimeUnit.SECONDS);


    def tearDown(self):
        self.driver.quit()


    def test_hello_world(self):
        print "getting"
        driver.get("https://0.0.0.0:5000/fetch")
        self.assertEquals("Hello Fetch!", driver.text)
