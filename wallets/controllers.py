
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
        return Wallets.get(login, base_currency).describe()

    @classmethod
    @response_format
    def get_wallets(cls, request: Request, **kwargs):
        """ Retreiving wallet's data """
        login = request.get("login")
        return Wallets.get_wallets(login)

    @classmethod
    @response_format
    def get_currencies(cls, request: Request, **kwargs):
        """ Retreiving list of supported currencies """
        return Wallets.get_currencies()

    @classmethod
    @response_format
    def topup(cls, request: Request, **kwargs):
        """ Top up wallet's balance """
        login = request.get("login")
        base_currency = request.get("base_currency", None)
        amount = int(request.get("amount", 0))
        return Wallets.top_up(login, base_currency, amount)

    @classmethod
    @response_format
    def transfer(cls, request: Request, **kwargs):
        """ Transfer funds from one wallet to another """
        from_login = request.get("from_login")
        from_base_currency = request.get("from_base_currency", None)
        to_login = request.get("to_login")
        to_base_currency = request.get("to_base_currency", None)
        amount = int(request.get("amount", 0))
        conversion_rate_uuid_1 = request.get("conversion_rate_uuid_1", None)
        conversion_rate_uuid_2 = request.get("conversion_rate_uuid_2", None)
        return Wallets.transfer(
            from_login, from_base_currency, to_login, to_base_currency,
            amount, conversion_rate_uuid_1, conversion_rate_uuid_2
        )
