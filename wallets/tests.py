import json
import unittest

from migrate import migrate
from envi import Request
from models import pool, Currencies
from controllers import DefaultController


class DefaultControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        with pool as db:
            db.execute_raw("DROP DATABASE IF EXISTS wallets")
            migrate(quiet=True)
            db.execute_raw("USE wallets")

    def test_wallets(self):
        # Creating:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)

        # Getting back:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.CNY, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

    def test_creating_on_demand(self):
        """ gracefull degradation: if someone authenticates with given login - we have to create a wallet for him """
        r = Request()
        r.set("login", "MyLogin")
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

    def test_supported_currencies(self):
        r = Request()
        self.assertEqual(
            {'1': "USD", '2': "EUR", '3': "CAD", '4': "CNY"},
            json.loads(DefaultController.get_currencies(r))["result"]
        )

        # Creating 4 wallets for ONE login (Supported currencies):
        for base_currency in [1, 2, 3, 4]:
            r = Request()
            r.set("login", f"MyLogin{base_currency}")
            r.set("base_currency", base_currency)
            result = json.loads(DefaultController.create(r))["result"]
            self.assertTrue(result)

        # Attempt to create unsupported wallet
        r = Request()
        r.set("login", "MyLoginBTC")
        r.set("base_currency", "BTC")
        self.assertEqual(
            {"code": "WALLETS_1", "message": "Unsupported Currency"},
            json.loads(DefaultController.create(r))["error"]
        )