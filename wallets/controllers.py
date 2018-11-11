
from envi import Controller, Request, response_format
from models import Wallets


# noinspection PyAbstractClass
class DefaultController(Controller):

    @classmethod
    @response_format
    def create(cls, request: Request, **kwargs):
        """ Creating new wallet """
        login = request.get("login")
        base_currency = request.get("base_currency", None)
        return Wallets.create(login, base_currency)

    @classmethod
    @response_format
    def get(cls, request: Request, **kwargs):
        """ Retreiving wallet's data """
        login = request.get("login")
        base_currency = request.get("base_currency", None)
        return Wallets.get(login, base_currency)

    @classmethod
    @response_format
    def get_currencies(cls, request: Request, **kwargs):
        """ Retreiving list of supported currencies """
        return Wallets.get_currencies()
