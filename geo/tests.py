import json
import unittest

from migrate import migrate
from envi import Request
from models import pool
from controllers import DefaultController


class DefaultControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        with pool as db:
            db.execute_raw("DROP DATABASE IF EXISTS geo")
            migrate(quiet=True)
            db.execute_raw("USE geo")

    def test_countries(self):

        # Request a country that doesn't exist yet
        r = Request()
        r.set("name", "Country1")
        self.assertEqual(
            {"id": 1, "name": "Country1"},
            json.loads(DefaultController.get_country(r))["result"]
        )

        # Request just created country by its id:
        r = Request()
        r.set("id", 1)
        self.assertEqual(
            {"id": 1, "name": "Country1"},
            json.loads(DefaultController.get_country(r))["result"]
        )

        # Request a country that doesn't exist by id:
        r = Request()
        r.set("id", 2)
        self.assertEqual(
            {"code": "GEO_1", "message": "Unknown country"},
            json.loads(DefaultController.get_country(r))["error"]
        )

    def test_cities(self):

        # Request a city with a country that doesn't exist
        r = Request()
        r.set("name", "City1")
        r.set("country_id", 1)
        self.assertEqual(
            {"code": "GEO_1", "message": "Unknown country"},
            json.loads(DefaultController.get_city(r))["error"]
        )

        # Create a country:
        r = Request()
        r.set("name", "Country1")
        self.assertEqual(
            {"id": 1, "name": "Country1"},
            json.loads(DefaultController.get_country(r))["result"]
        )

        # Request a city that doesn't exist with just created country:
        r = Request()
        r.set("name", "City1")
        r.set("country_id", 1)
        self.assertEqual(
            {"id": 1, "name": "City1", "country_id": 1},
            json.loads(DefaultController.get_city(r))["result"]
        )

        # Request a city that doesn't exist by id:
        r = Request()
        r.set("id", 2)
        r.set("country_id", 1)
        self.assertEqual(
            {"code": "GEO_2", "message": "Unknown city"},
            json.loads(DefaultController.get_city(r))["error"]
        )