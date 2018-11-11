
import os
from mapex import EntityModel, CollectionModel, SqlMapper, Pool, MySqlClient
from exceptions import UnsupportedCurrency


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
            self.int("balance", "Balance")                 # cents or fens
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
        Wallets.get(login, base_currency)
        return True

    @staticmethod
    def get(login: str, base_currency: int = None):
        if not base_currency:
            base_currency = Currencies.USD
        else:
            if not base_currency in list(Currencies.NAMES.keys()):
                raise UnsupportedCurrency()

        bounds = {"login": login, "base_currency": base_currency}
        wallet = Wallets().get_item(bounds) or Wallet({**bounds, "balance": 0}).save()
        return wallet.describe()

    @staticmethod
    def get_currencies() -> dict:
        return Currencies.NAMES