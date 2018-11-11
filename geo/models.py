""" Модели """

import os
from mapex import EntityModel, CollectionModel, SqlMapper, Pool, MySqlClient
from exceptions import CountryNotFound, CityNotFound


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


class CountriesMapper(SqlMapper):
    """ describes relations between py-models and database structure """
    pool = pool

    def bind(self):
        self.set_new_item(Country)
        self.set_new_collection(Countries)
        self.set_collection_name("countries")
        self.set_map([
            self.int("id", "ID"),
            self.str("name", "Name")
        ])


class Country(EntityModel):
    """ represents single country record """
    mapper = CountriesMapper

    def describe(self):
        return self.stringify(["id", "name"])


class Countries(CollectionModel):
    """ represents all the countries """
    mapper = CountriesMapper

    @staticmethod
    def get(country_id: int=None, country_name: str=None) -> dict:
        """ Get country by its id or name """
        if country_id:
            country = Countries().get_item({"id": country_id})
            if not country:
                raise CountryNotFound()
        else:
            country = Countries().get_item({"name": country_name}) or Country({"name": country_name}).save()

        return country.describe()


class CitiesMapper(SqlMapper):
    """ describes relations between py-models and database structure """
    pool = pool

    def bind(self):
        self.set_new_item(City)
        self.set_new_collection(Cities)
        self.set_collection_name("cities")
        self.set_map([
            self.int("id", "ID"),
            self.str("name", "Name"),
            self.int("country_id", "CountryID")
        ])


class City(EntityModel):
    """ represents single city record """
    mapper = CitiesMapper

    def describe(self):
        return self.stringify(["id", "name", "country_id"])


class Cities(CollectionModel):
    """ represents all the cities """
    mapper = CitiesMapper

    @staticmethod
    def get(country_id: int, city_id: int = None, city_name: str = None) -> dict:
        """ Get city by its it or name """

        # First, check if country exists:
        country = Countries().get_item({"id": country_id})
        if not country:
            raise CountryNotFound()


        if city_id:
            city = Cities().get_item({"id": city_id, "country_id": country_id})
            if not city:
                raise CityNotFound()
        else:
            bounds = {"name": city_name, "country_id": country_id}
            city = Cities().get_item(bounds) or City(bounds).save()

        return city.describe()