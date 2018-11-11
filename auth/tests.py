import json
import unittest

from migrate import migrate
from envi import Request
from models import pool, CredentialsRecord, CredentialsRecords
from controllers import DefaultController


class DefaultControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        with pool as db:
            db.execute_raw("DROP DATABASE IF EXISTS auth")
            migrate(quiet=True)
            db.execute_raw("USE auth")

    def test_success_scenario(self):
        # Registration:
        r = Request()
        r.set("login", 'MyLogin')
        r.set("password", "MySecret")
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)

        # Authentication:
        r = Request()
        r.set("login", 'MyLogin')
        r.set("password", "MySecret")
        token1 = json.loads(DefaultController.auth(r))["result"]
        # We got a token 32-symbols length
        self.assertEqual(32, len(token1))

        # Second authentication provides as with same-length token:
        token2 = json.loads(DefaultController.auth(r))["result"]
        self.assertEqual(32, len(token2))

        # But this time it is not equal with the first one:
        self.assertNotEqual(token1, token2)

        # Authentication with token:
        r = Request()
        r.set("token", token2)
        result = json.loads(DefaultController.auth(r))["result"]
        self.assertTrue(result)

    def test_wrong_credentials(self):
        """ common test with entity `credentials` """

        # Registration:
        r = Request()
        r.set("login", 'MyLogin')
        r.set("password", "MySecret")
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)

        # Second attempt to register with the same login:
        r = Request()
        r.set("login", 'MyLogin')
        r.set("password", "MySecret")
        self.assertEqual(
            {"error": {"code": "DC_AUTH_4", "message": "Already registred"}},
            json.loads(DefaultController.create(r))
        )

        # Authetntication with incorrect login:
        r = Request()
        r.set("login", 'BadLogin')
        r.set("password", "MySecret")
        self.assertEqual(
            {"error": {"code": "DC_AUTH_1", "message": "Incorrect login"}},
            json.loads(DefaultController.auth(r))
        )

        # Authetntication with incorrect password:
        r = Request()
        r.set("login", 'MyLogin')
        r.set("password", "BadPassword")
        self.assertEqual(
            {"error": {"code": "DC_AUTH_2", "message": "Incorrect password"}},
            json.loads(DefaultController.auth(r))
        )

        # Authentication with incorrect token:
        r = Request()
        r.set("token", "BadToken")
        self.assertEqual(
            {"error": {"code": "DC_AUTH_3", "message": "Incorrect token"}},
            json.loads(DefaultController.auth(r))
        )