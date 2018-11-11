
from envi import Controller, Request, response_format
from models import Countries, Cities


# noinspection PyAbstractClass
class DefaultController(Controller):

    @classmethod
    @response_format
    def get_country(cls, request: Request, **kwargs):
        """ Retreiving country """
        country_id = request.get("id", None)
        name = request.get("name", None)
        return Countries.get(country_id, name)

    @classmethod
    @response_format
    def get_city(cls, request: Request, **kwargs):
        """ Retreiving city """
        city_id = request.get("id", None)
        name = request.get("name", None)
        country_id = request.get("country_id", None)
        return Cities.get(country_id, city_id, name)
