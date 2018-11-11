
import os
from uuid import uuid4
from datetime import datetime, timedelta
from clickhouse_driver.client import Client as ClickHouseClient

from envi import microservice
from mapex import EntityModel, CollectionModel, SqlMapper, Pool, MySqlClient
from exceptions import UnsupportedCurrency, WalletNotFound, InsufficientFunds, NoConversionRateProvided
from exceptions import ConvertionRateExpired, InvalidConvertionRate


# define connection pool for database:
pool = Pool(
    MySqlClient,
    (
        os.environ.get("MYSQL_HOST"),
        os.environ.get("MYSQL_PORT"),
        os.environ.get("MYSQL_USER"),
        os.environ.get("MYSQL_PASS"),
        os.environ.get("MYSQL_DBNAME")
    )
)


class Currencies:

    # How fresh provided convertion-rate-object should be (seconds):
    CONVERSION_RATE_TIMEOUT_TOLERANCE=30

    USD = 1
    EUR = 2
    CAD = 3
    CNY = 4

    NAMES = {
        USD: "USD",
        EUR: "EUR",
        CAD: "CAD",
        CNY: "CNY"
    }

    class Converter:
        """
        Utility class for working with currencies and and convertion rates
        """
        get_last_value = lambda bc: microservice("http://converter/get_last_value", {"base_currency": bc}, "result")
        get_by_uuid = lambda uuid: microservice("http://converter/get_by_uuid", {"uuid": uuid}, "result")

        @staticmethod
        def get_convertion_rate_value(original_currency, convertion_rate_uuid):
            """ Retrieving and validation convertion rate """
            # noinspection PyCallByClass
            conversion_rate = Currencies.Converter.get_by_uuid(convertion_rate_uuid)
            conversion_rate_datetime = datetime.strptime(conversion_rate["datetime"], "%c")
            convertion_rate_expired_datetime = datetime.now() - timedelta(
                seconds=Currencies.CONVERSION_RATE_TIMEOUT_TOLERANCE
            )
            if conversion_rate_datetime < convertion_rate_expired_datetime:
                raise ConvertionRateExpired()

            if conversion_rate["base_currency"] != original_currency:
                raise InvalidConvertionRate()

            return conversion_rate["value"]

        @staticmethod
        def convert(
                amount: float,
                from_base_currency: int, to_base_currency: int,
                convertion_rate_uuid_1: str=None, convertion_rate_uuid_2: str=None) -> float:
            """ Converts currencies based on given convertion rates with validation """

            # No convertion required:
            if from_base_currency == to_base_currency:
                convertion_rate_value_1 = 1
                convertion_rate_value_2 = 1

            # At least one convertion required:
            else:
                # From USD to Other Currency (1 convertion):
                if from_base_currency == Currencies.USD:
                    convertion_rate_value_1 = 1
                    if not convertion_rate_uuid_2:
                        raise NoConversionRateProvided()
                    else:
                        convertion_rate_value_2 = Currencies.Converter.get_convertion_rate_value(
                            to_base_currency, convertion_rate_uuid_2
                        )
                # From Some Currency to USD (1 convertion):
                elif to_base_currency == Currencies.USD:
                    convertion_rate_value_2 = 1
                    if not convertion_rate_uuid_1:
                        raise NoConversionRateProvided()
                    else:
                        convertion_rate_value_1 = Currencies.Converter.get_convertion_rate_value(
                            from_base_currency, convertion_rate_uuid_1
                        )
                # From Some Currency to Other Currency, not USD (2 convertions):
                else:
                    if not convertion_rate_uuid_1 or not convertion_rate_uuid_2:
                        raise NoConversionRateProvided()
                    convertion_rate_value_1 = Currencies.Converter.get_convertion_rate_value(
                        from_base_currency, convertion_rate_uuid_1
                    )
                    convertion_rate_value_2 = Currencies.Converter.get_convertion_rate_value(
                        to_base_currency, convertion_rate_uuid_2
                    )

            return amount * convertion_rate_value_1 / convertion_rate_value_2


class WalletsMapper(SqlMapper):
    """ describes relations between py-models and database structure """
    pool = pool

    def bind(self):
        self.set_new_item(Wallet)
        self.set_new_collection(Wallets)
        self.set_collection_name("wallets")
        self.set_map([
            self.str("login", "Login"),
            self.int("base_currency", "BaseCurrency"),
            self.float("balance", "Balance")             # cents or fens
        ])
        self.set_primary(["login", "base_currency"])


class Wallet(EntityModel):
    """ represents single wallet """
    mapper = WalletsMapper

    def describe(self):
        return self.stringify(["login", "base_currency", "balance"])


class Wallets(CollectionModel):
    """ represents all the wallets """
    mapper = WalletsMapper

    @staticmethod
    def create(login: str, base_currency: int=None):
        """ Creates new `base_currency` wallet for `login` """
        Wallets.get(login, base_currency)
        return True

    @staticmethod
    def get(login: str, base_currency: int=None):
        """ Retrieves `base_currency` wallet for `login` """
        if not base_currency:
            base_currency = Currencies.USD
        else:
            if not base_currency in list(Currencies.NAMES.keys()):
                raise UnsupportedCurrency()

        bounds = {"login": login, "base_currency": base_currency}
        wallet = Wallets().get_item(bounds) or Wallet({**bounds, "balance": 0}).save()
        return wallet

    @staticmethod
    def get_wallets(login: str):
        """ Retrieves all wallets for `login` """
        bounds = {"login": login}
        return [w.describe() for w in Wallets().get_items(bounds)]

    @staticmethod
    def get_currencies() -> dict:
        """ Retrieves all supported base currencies (codes and names) """
        return Currencies.NAMES

    @staticmethod
    def top_up(login: str, base_currency, amount) -> bool:
        """ Tops up `base_currency` wallet for `login` by given amount of money """

        with Wallets.mapper.pool.transaction:
            wallet = Wallets().get_item({"login": login, "base_currency": base_currency})
            if not wallet:
                raise WalletNotFound()
            wallet.balance += amount
            wallet.save()
        return True

    @staticmethod
    def transfer(
            from_login: str, from_base_currency: int,
            to_login: str, to_base_currency: int,
            amount: int, convertion_rate_uuid_1: str=None, convertion_rate_uuid_2: str=None) -> dict:
        """ Transfers certain amount of money from one wallet to another """

        with Wallets.mapper.pool.transaction:
            from_wallet = Wallets().get_item({"login": from_login, "base_currency": from_base_currency})
            to_wallet = Wallets().get_item({"login": to_login, "base_currency": to_base_currency})

            if not from_wallet or not to_wallet:
                raise WalletNotFound()

            if amount <= from_wallet.balance:

                converted_amount = Currencies.Converter.convert(
                    amount,
                    from_base_currency, to_base_currency,
                    convertion_rate_uuid_1, convertion_rate_uuid_2
                )

                from_wallet.balance -= amount
                to_wallet.balance += converted_amount
                from_wallet.save()
                to_wallet.save()

                # Everything is ok, but we need to save transaction log
                # if this fails - the whole sql-tx will be rolled back automatically:
                tx_uuid = str(uuid4())
                tx_datetime = datetime.now()

                ClickHouse.save_transaction(
                    tx_uuid,
                    from_login, from_base_currency, to_login, to_base_currency,
                    amount, converted_amount, convertion_rate_uuid_1, convertion_rate_uuid_2,
                    tx_datetime
                )

                return {"uuid": tx_uuid, "datetime": tx_datetime}
            else:
                raise InsufficientFunds()
    @staticmethod
    def get_transactions(login: str, period_starts=None, period_ends=None):
        return ClickHouse.get_transactions(login, period_starts, period_ends)

class ClickHouse:

    def __init__(self):
        if os.environ.get("DEPLOY_MODE") != "PROD":
            self.client = ClickHouseClient('clickhouse')
        else:
            host = os.environ.get("CLICKHOUSE_HOST")
            port = os.environ.get("CLICKHOUSE_PORT")
            user = os.environ.get("CLICKHOUSE_USER")
            pasw = os.environ.get("CLICKHOUSE_PASSWORD")
            self.client = ClickHouseClient(host, port=port, user=user, password=pasw)

    def execute(self, query: str, data=None):
        return self.client.execute(query, data)

    def disconnect(self):
        self.client.disconnect()

    @staticmethod
    def save_transaction(
            tx_uuid: str,
            from_login: str, from_base_currency: int,
            to_login: str, to_base_currency: int,
            original_amount: float, converted_amount: float,
            cr_uuid1: str, cr_uuid2: str, dt):
        """ Saving transaction for the history and reports """
        clickhouse = ClickHouse()
        clickhouse.execute(
            "INSERT INTO `outgoing_transactions` "
            "(`tx_uuid`, `login`, `base_currency`, `amount`, `cr_uuid`, `datetime`) "
            "VALUES",
            [
                {
                    "tx_uuid": tx_uuid,
                    "login": from_login,
                    "base_currency": from_base_currency,
                    "amount": original_amount,
                    "cr_uuid": cr_uuid1 or "",
                    "datetime": dt
                }
            ]
        )
        clickhouse.execute(
            "INSERT INTO `incoming_transactions` "
            "(`tx_uuid`, `login`, `base_currency`, `amount`, `cr_uuid`, `datetime`) "
            "VALUES",
            [
                {
                    "tx_uuid": tx_uuid,
                    "login": to_login,
                    "base_currency": to_base_currency,
                    "amount": converted_amount,
                    "cr_uuid": cr_uuid2 or "",
                    "datetime": dt
                }
            ]
        )
        clickhouse.disconnect()
        return True

    @staticmethod
    def get_transactions(login: str, period_starts=None, period_ends=None):
        """ Getting transactions history for reports """

        period_starts_bounds, period_ends_bounds = "", ""

        if period_starts:
            period_starts_bounds = " and `datetime` > '{period_starts.isoformat()}' "

        if period_ends:
            period_ends_bounds = " and `datetime` < '{period_ends.isoformat()}' "

        clickhouse = ClickHouse()
        incoming = clickhouse.execute(f"""
            SELECT 
            `tx_uuid`, `login`, `base_currency`, round(`amount`, 4), `cr_uuid`, `datetime`
            FROM `incoming_transactions` WHERE login = '{login}' 
            {period_starts_bounds} {period_ends_bounds}
        """)

        outgoing = clickhouse.execute(f"""
            SELECT 
            `tx_uuid`, `login`, `base_currency`, round(`amount`, 4), `cr_uuid`, `datetime`
            FROM `outgoing_transactions` WHERE login = '{login}' 
            {period_starts_bounds} {period_ends_bounds}
        """)
        clickhouse.disconnect()

        return {
            "incoming": incoming,
            "outgoing": outgoing
        }
