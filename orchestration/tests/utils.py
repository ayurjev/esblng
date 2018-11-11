
import os
import unittest
import time
import mysql.connector
from clickhouse_driver.client import Client as ClickHouseClient


class TestWrapper(unittest.TestCase):

    mysql_config = {
        'host': 'db',
        'port': 3306,
        'user': 'root',
        'password': ''
    }

    mysql_databases = [
        "auth",
        "geo",
        "users",
        "wallets"
    ]
    exclude_tables = ['migrations']

    def setUp(self):
        self.startTime = time.time()
        self.maxDiff = None
        self.reset_clickhouse()
        self.reset_mysql()
        time.sleep(0.5)

    def reset_mysql(self):
        cnx = mysql.connector.connect(**self.mysql_config)
        cursor = cnx.cursor()
        for database in self.mysql_databases:
            query = """SHOW TABLES in `%s`""" % database
            cursor.execute(query)
            tables = cursor.fetchall()
            for table in tables:
                if table[0] not in self.exclude_tables:
                    q = """TRUNCATE %s.%s""" % (database, table[0])
                    cursor.execute(q)
        cnx.commit()
        cursor.close()
        cnx.close()

    @staticmethod
    def reset_clickhouse():
        clickhouse_manager = ClickHouseManager()
        clickhouse_manager.execute(f"DROP TABLE IF EXISTS `rates_revisions`")
        clickhouse_manager.execute(f"DROP TABLE IF EXISTS `incoming_transactions`")
        clickhouse_manager.execute(f"DROP TABLE IF EXISTS `outgoing_transactions`")
        clickhouse_manager.execute("""
            CREATE TABLE IF NOT EXISTS `rates_revisions`
            (
                uuid String,
                base_currency Int8,
                value Float64,
                datetime Datetime,
                inserted Datetime DEFAULT now()
            )
            ENGINE MergeTree()
            PARTITION BY (datetime)
            ORDER BY (base_currency, datetime) SETTINGS index_granularity=8192
            """
        )

        clickhouse_manager.execute("""
            CREATE TABLE IF NOT EXISTS `incoming_transactions`
            (
                tx_uuid String,
                login String,
                base_currency Int8,
                amount Float64,
                cr_uuid String,
                datetime Datetime
            )
            ENGINE MergeTree()
            PARTITION BY (datetime)
            ORDER BY (login, datetime) SETTINGS index_granularity=8192;
        """)

        clickhouse_manager.execute("""
            CREATE TABLE IF NOT EXISTS `outgoing_transactions`
            (
                tx_uuid String,
                login String,
                base_currency Int8,
                amount Float64,
                cr_uuid String,
                datetime Datetime
            )
            ENGINE MergeTree()
            PARTITION BY (datetime)
            ORDER BY (login, datetime) SETTINGS index_granularity=8192;
        """)


class ClickHouseManager:
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


if __name__ == '__main__':
    tw = TestWrapper()
    tw.reset_clickhouse()
    print("tables created", flush=True)
