import json
import unittest
from datetime import datetime

from migrate import migrate
from envi import Request
from models import pool, Currencies, ClickHouse
from controllers import DefaultController


class DefaultControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        with pool as db:
            db.execute_raw("DROP DATABASE IF EXISTS wallets")
            migrate(quiet=True)
            db.execute_raw("USE wallets")

        self.clickhouse = ClickHouse()
        self.clickhouse.execute('''DROP TABLE IF EXISTS `outgoing_transactions`''')
        self.clickhouse.execute('''DROP TABLE IF EXISTS `incoming_transactions`''')
        with open("clickhouse_migrations/01-incoming-transactions.sql") as f:
            self.clickhouse.execute("".join(f.readlines()))
        with open("clickhouse_migrations/02-outgoing-transactions.sql") as f:
            self.clickhouse.execute("".join(f.readlines()))

    def tearDown(self):
        self.clickhouse.disconnect()

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

    def test_topup_wallet_balance(self):
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)

        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        r.set("amount", 100)
        result = json.loads(DefaultController.topup(r))["result"]
        self.assertTrue(result)

        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 100},
            json.loads(DefaultController.get(r))["result"]
        )

    def test_successful_transfer_between_wallets_USD_TO_USD(self):

        # Create first empty wallet with USD:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Create seconds empty wallet with USD:
        r = Request()
        r.set("login", "MyLogin2")
        r.set("base_currency", Currencies.USD)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin2", "base_currency": Currencies.USD, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Top up first wallet with some 1 USD
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        r.set("amount", 100)
        result = json.loads(DefaultController.topup(r))["result"]
        self.assertTrue(result)

        # Transfer funds:
        r = Request()
        r.set("from_login", "MyLogin")
        r.set("from_base_currency", Currencies.USD)
        r.set("to_login", "MyLogin2")
        r.set("to_base_currency", Currencies.USD)
        r.set("amount", 50)
        result = json.loads(DefaultController.transfer(r))["result"]
        self.assertTrue(result)

        # Check:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 50},
            json.loads(DefaultController.get(r))["result"]
        )
        r.set("base_currency", Currencies.USD)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 50},
            json.loads(DefaultController.get(r))["result"]
        )

    def test_successful_transfer_between_wallets_USD_TO_CNY(self):

        # We need a mock for converter:
        class MockConverter(Currencies.Converter):
            get_last_value = lambda bc: 0.25
            get_by_uuid = lambda uuid: {
                "uuid": uuid, "value": 0.25,
                "base_currency": Currencies.CNY, "datetime": datetime.now().strftime("%c")
            }

        # Set up our mock:
        Currencies.Converter = MockConverter

        # Create first empty wallet with USD:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Create seconds empty wallet with CNY:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.CNY, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Top up first wallet with some 100 USD
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        r.set("amount", 100)
        result = json.loads(DefaultController.topup(r))["result"]
        self.assertTrue(result)

        # Transfer funds:
        r = Request()
        r.set("from_login", "MyLogin")
        r.set("from_base_currency", Currencies.USD)
        r.set("to_login", "MyLogin")
        r.set("to_base_currency", Currencies.CNY)
        r.set("conversion_rate_uuid_1", None)
        r.set("conversion_rate_uuid_2", "576ff813-d370-475d-aa02-c576ef291b96")
        r.set("amount", 50)
        result = json.loads(DefaultController.transfer(r))["result"]
        self.assertTrue(result)

        # Check:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 50},
            json.loads(DefaultController.get(r))["result"]
        )
        r.set("base_currency", Currencies.CNY)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.CNY, "balance": 200},
            json.loads(DefaultController.get(r))["result"]
        )

    def test_successful_transfer_between_wallets_CNY_TO_USD(self):

        # We need a mock for converter:
        class MockConverter(Currencies.Converter):
            get_last_value = lambda bc: 0.25
            get_by_uuid = lambda uuid: {
                "uuid": uuid, "value": 0.25,
                "base_currency": Currencies.CNY, "datetime": datetime.now().strftime("%c")
            }

        # Set up our mock:
        Currencies.Converter = MockConverter

        # Create first empty wallet with USD:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.CNY, "balance": 0.0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Create seconds empty wallet with USD:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 0.0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Top up first wallet with some 10 CNY
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        r.set("amount", 10)
        result = json.loads(DefaultController.topup(r))["result"]
        self.assertTrue(result)

        # Transfer funds:
        r = Request()
        r.set("from_login", "MyLogin")
        r.set("from_base_currency", Currencies.CNY)
        r.set("to_login", "MyLogin")
        r.set("to_base_currency", Currencies.USD)
        r.set("conversion_rate_uuid_1", "576ff813-d370-475d-aa02-c576ef291b96")
        r.set("conversion_rate_uuid_2", None)
        r.set("amount", 10)
        result = json.loads(DefaultController.transfer(r))["result"]
        self.assertTrue(result)

        # Check:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.CNY, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )
        r.set("base_currency", Currencies.USD)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 2.5},
            json.loads(DefaultController.get(r))["result"]
        )

    def test_successful_transfer_between_wallets_CNY_TO_EUR(self):

        # We need a mock for converter:
        class MockConverter(Currencies.Converter):
            get_last_value = lambda bc: 0.25 if bc == Currencies.CNY else 1.2
            get_by_uuid = lambda uuid: {
                "uuid": uuid, "value": 0.25 if uuid == "CNY-USD" else 1.2,
                "base_currency": Currencies.CNY if uuid == "CNY-USD" else Currencies.EUR,
                "datetime": datetime.now().strftime("%c")
            }

        # Set up our mock:
        Currencies.Converter = MockConverter

        # Create first empty wallet with CNY:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.CNY, "balance": 0.0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Create seconds empty wallet with EUR:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.EUR)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.EUR, "balance": 0.0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Top up first wallet with some 10 CNY
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        r.set("amount", 10)
        result = json.loads(DefaultController.topup(r))["result"]
        self.assertTrue(result)

        # Transfer funds:
        r = Request()
        r.set("from_login", "MyLogin")
        r.set("from_base_currency", Currencies.CNY)
        r.set("to_login", "MyLogin")
        r.set("to_base_currency", Currencies.EUR)
        r.set("conversion_rate_uuid_1", "CNY-USD")
        r.set("conversion_rate_uuid_2", "USD-EUR")
        r.set("amount", 10)
        tx_result = json.loads(DefaultController.transfer(r))["result"]
        tx_uuid = tx_result["uuid"]
        tx_datetime = tx_result["datetime"]
        self.assertEqual(36, len(tx_uuid))

        # Check:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.CNY)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.CNY, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )
        r.set("base_currency", Currencies.EUR)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.EUR, "balance": 2.0833},
            json.loads(DefaultController.get(r))["result"]
        )

        # Check reports:
        r = Request()
        r.set("login", "MyLogin")
        self.assertEqual(
            {
                "incoming": [
                    [tx_uuid, "MyLogin", Currencies.EUR, 2.0833, "USD-EUR", tx_datetime]
                ],
                "outgoing": [
                    [tx_uuid, "MyLogin", Currencies.CNY, 10.0, "CNY-USD", tx_datetime]
                ],
            },
            json.loads(DefaultController.get_transactions(r))["result"]
        )



    def test_insufficient_funds(self):
        # Create first empty wallet with USD:
        r = Request()
        r.set("login", "MyLogin")
        r.set("base_currency", Currencies.USD)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin", "base_currency": Currencies.USD, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Create seconds empty wallet with USD:
        r = Request()
        r.set("login", "MyLogin2")
        r.set("base_currency", Currencies.USD)
        result = json.loads(DefaultController.create(r))["result"]
        self.assertTrue(result)
        self.assertEqual(
            {"login": "MyLogin2", "base_currency": Currencies.USD, "balance": 0},
            json.loads(DefaultController.get(r))["result"]
        )

        # Test rejection:
        r = Request()
        r.set("from_login", "MyLogin")
        r.set("from_base_currency", Currencies.USD)
        r.set("to_login", "MyLogin")
        r.set("to_base_currency", Currencies.USD)
        r.set("amount", 1)
        self.assertEqual(
            {"error": {"code": "WALLETS_3", "message": "Insufficient Funds"}},
            json.loads(DefaultController.transfer(r))
        )
