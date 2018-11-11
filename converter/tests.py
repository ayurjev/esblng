import json
import unittest

from datetime import datetime

from envi import Request
from models import ClickHouse, Currencies
from controllers import DefaultController


class DefaultControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        ClickHouse().execute('''DROP TABLE IF EXISTS `rates_revisions`''')
        with open("migrations/01-initial.sql") as f:
            ClickHouse().execute("".join(f.readlines()))

    def test_success_scenario(self):
        # Saving rates:
        r = Request()
        r.set("base_currency", Currencies.EUR)
        r.set("value", 1.246778)
        self.assertTrue(json.loads(DefaultController.save(r))["result"])

        r = Request()
        r.set("base_currency", Currencies.CNY)
        r.set("value", 3.467789)
        self.assertTrue(json.loads(DefaultController.save(r))["result"])

        # Get last value:
        r = Request()
        r.set("base_currency", Currencies.CNY)
        last_value = json.loads(DefaultController.get_last_value(r))["result"]
        self.assertEqual(
            {"uuid": last_value["uuid"], "value": 3.467789, "base_currency": Currencies.CNY},
            last_value
        )

        r = Request()
        r.set("base_currency", Currencies.EUR)
        last_value = json.loads(DefaultController.get_last_value(r))["result"]
        self.assertEqual(
            {"uuid": last_value["uuid"], "value": 1.246778, "base_currency": Currencies.EUR},
            last_value
        )

        # Get by uuid:
        r = Request()
        r.set("uuid", last_value["uuid"])
        last_value = json.loads(DefaultController.get_by_uuid(r))["result"]
        self.assertEqual(
            {"uuid": last_value["uuid"], "value": 1.246778, "base_currency": Currencies.EUR},
            last_value
        )

    def test_no_data(self):
        r = Request()
        r.set("base_currency", Currencies.EUR)
        self.assertEqual(
            {"error": {"code": "CONVERTER_1", "message": "No Data For Requested Currency"}},
            json.loads(DefaultController.get_last_value(r))
        )

    def test_bulk_upload(self):
        r = Request()
        r.set("data", [
            {"base_currency": Currencies.EUR, "value": 1.2, "datetime": datetime.now().strftime("%c")},
            {"base_currency": Currencies.CNY, "value": 3.4, "datetime": datetime.now().strftime("%c")},
        ])
        self.assertTrue(json.loads(DefaultController.save_bulk(r))["result"])

        r = Request()
        r.set("base_currency", Currencies.EUR)
        last_value = json.loads(DefaultController.get_last_value(r))["result"]
        self.assertEqual(
            {"uuid": last_value["uuid"], "value": 1.2, "base_currency": Currencies.EUR},
            last_value
        )

        r = Request()
        r.set("base_currency", Currencies.CNY)
        last_value = json.loads(DefaultController.get_last_value(r))["result"]
        self.assertEqual(
            {"uuid": last_value["uuid"], "value": 3.4, "base_currency": Currencies.CNY},
            last_value
        )