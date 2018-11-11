
from envi import Controller, Request, response_format
from models import Users


# noinspection PyAbstractClass
class DefaultController(Controller):

    @classmethod
    @response_format
    def create(cls, request: Request, **kwargs):
        """ Creating new user """
        login = request.get("login")
        name = request.get("name")
        country_id = int(request.get("country_id")) if request.get("country_id", None) else None
        city_id = int(request.get("city_id")) if request.get("city_id", None) else None
        return Users.create(login, name, country_id, city_id)

    @classmethod
    @response_format
    def change(cls, request: Request, **kwargs):
        """ Updating user's data """
        login = request.get("login")
        name = request.get("name", None)
        country_id = int(request.get("country_id")) if request.get("country_id", None) else None
        city_id = int(request.get("city_id")) if request.get("city_id", None) else None
        return Users.change(login, name, country_id, city_id)

    @classmethod
    @response_format
    def get(cls, request: Request, **kwargs):
        """ Retreiving user's data """
        login = request.get("login")
        return Users.get(login)
