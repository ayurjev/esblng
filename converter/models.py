""" Модели """

import os
from uuid import uuid4
from datetime import datetime
from clickhouse_driver.client import Client as ClickHouseClient
from exceptions import UnknownRatesInformation


class Currencies:
    USD = 1
    EUR = 2
    CAD = 3
    CNY = 4

    NAMES = {
        USD: "USD",
        EUR: "EUR",
        CAD: "CAD",
        CNY: "CNY",
    }


class ClickHouse:
    @staticmethod
    def execute(query: str, data=None):
        if os.environ.get("DEPLOY_MODE") != "PROD":
            client = ClickHouseClient('clickhouse')
        else:
            host = os.environ.get("CLICKHOUSE_HOST")
            port = os.environ.get("CLICKHOUSE_PORT")
            user = os.environ.get("CLICKHOUSE_USER")
            pasw = os.environ.get("CLICKHOUSE_PASSWORD")
            client = ClickHouseClient(host, port=port, user=user, password=pasw)
        res = client.execute(query, data)
        client.disconnect()
        return res

    @staticmethod
    def save(base_currency: int, value: float, dt: str=None):
        ClickHouse().execute(
            "INSERT INTO `rates_revisions` (`uuid`, `base_currency`, `value`, `datetime`) VALUES",
            [
                {
                    "uuid": str(uuid4()),
                    "base_currency": base_currency,
                    "value": value,
                    "datetime": datetime.strptime(dt, "%c") if dt else datetime.now()
                }
            ]
        )
        return True

    @staticmethod
    def save_bulk(data: list):
        ClickHouse().execute(
            "INSERT INTO `rates_revisions` (`uuid`, `base_currency`, `value`, `datetime`) VALUES",
            [
                {
                    "uuid": str(uuid4()),
                    "base_currency": record["base_currency"],
                    "value": record["value"],
                    "datetime": datetime.strptime(record["datetime"], "%c")
                    if record.get("datetime") else datetime.now()
                }
                for record in data
            ]
        )
        return True

    @staticmethod
    def get_last_value(base_currency: int):
        res = ClickHouse().execute(
            "SELECT `uuid`, `value`, `datetime` FROM `rates_revisions` WHERE `base_currency` = %d "
            "ORDER BY `datetime`, `inserted` DESC LIMIT 1"
            "" % base_currency
        )
        if res:
            return {"uuid": res[0][0], "value": res[0][1], "base_currency": base_currency, "datetime": res[0][2]}
        else:
            raise UnknownRatesInformation()

    @staticmethod
    def get_by_uuid(uuid: str):
        res = ClickHouse().execute(
            "SELECT `base_currency`, `value`, `datetime` FROM `rates_revisions` WHERE `uuid` = '%s' LIMIT 1" % (
                uuid.encode().decode('unicode_escape')
            )
        )
        if res:
            return {"uuid": uuid, "value": res[0][1], "base_currency": res[0][0], "datetime": res[0][2]}
        else:
            raise UnknownRatesInformation()