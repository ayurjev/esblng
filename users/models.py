""" Модели """

import os
from mapex import EntityModel, CollectionModel, SqlMapper, Pool, MySqlClient


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


class UsersMapper(SqlMapper):
    """ describes relations between py-models and database structure """
    pool = pool

    def bind(self):
        self.set_new_item(User)
        self.set_new_collection(Users)
        self.set_collection_name("users")
        self.set_map([
            self.str("login", "Login"),
            self.str("name", "Name"),
            self.int("country_id", "CountryID"),
            self.int("city_id", "CityID")
        ])
        self.set_primary("login")


class User(EntityModel):
    """ represents single user """
    mapper = UsersMapper

    def describe(self):
        return self.stringify(["login", "name", "country_id", "city_id"])


class Users(CollectionModel):
    """ represents all the users """
    mapper = UsersMapper

    @staticmethod
    def create(login: str, name: str=None, country_id: int=None, city_id:int=None) -> bool:
        """ creates new user with given information """
        user = Users().get_item({"login": login}) or User({"login": login})
        user.name = name
        user.country_id = country_id
        user.city_id = city_id
        user.save()
        return True

    @staticmethod
    def change(login: str, name: str=None, country_id: int=None, city_id:int=None) -> bool:
        """ updates user's data with given information """
        user = Users().get_item({"login": login}) or User({"login": login})
        user.name = name if name else user.name
        user.country_id = country_id if country_id else user.country_id
        user.city_id = city_id if city_id else user.city_id
        user.save()
        return True

    @staticmethod
    def get(login: str) -> dict:
        """ get user's data or create new one (in case user doesn't exist) """
        user = Users().get_item({"login": login}) or User({"login": login, "name": "Unknown"}).save()
        return user.describe()