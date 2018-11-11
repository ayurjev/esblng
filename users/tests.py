import json
import unittest

from migrate import migrate
from envi import Request
from models import pool, User, Users
from controllers import DefaultController


class DefaultControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        with pool as db:
            db.execute_raw("DROP DATABASE IF EXISTS users")
            migrate(quiet=True)
            db.execute_raw("USE users")

    def test_users(self):
        # Creating:
        r = Request()
        r.set("login", "MyLogin")
        r.set("name", "MyName")
        r.set("country_id", 1)
        r.set("city_id", 2)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)

        # Getting back:
        r = Request()
        r.set("login", "MyLogin")
        self.assertEqual(
            {"login": "MyLogin", "name": "MyName", "country_id": 1, "city_id": 2},
            json.loads(DefaultController.get(r))["result"]
        )

        # Updating:
        r = Request()
        r.set("login", "MyLogin")
        r.set("name", "MyName Updated")
        r.set("country_id", 11)
        r.set("city_id", 22)
        result = json.loads(DefaultController.change(r))["result"]
        self.assertTrue(result)

        # Check:
        r = Request()
        r.set("login", "MyLogin")
        self.assertEqual(
            {"login": "MyLogin", "name": "MyName Updated", "country_id": 11, "city_id": 22},
            json.loads(DefaultController.get(r))["result"]
        )

    def test_creating_on_demand(self):
        """ gracefull degradation: if someone authenticates with given login - we have to create a user for him """
        r = Request()
        r.set("login", "MyLogin")
        self.assertEqual(
            {"login": "MyLogin", "name": "Unknown", "country_id": None, "city_id": None},
            json.loads(DefaultController.get(r))["result"]
        )
