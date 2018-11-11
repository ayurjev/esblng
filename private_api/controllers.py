from envi import Controller, Request, microservice, response_format
from utils import cors


# noinspection PyPep8Naming,PyAbstractClass
class DefaultPrivateController(Controller):

    @classmethod
    @cors
    @response_format
    def topUpBalance(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        login = request.get("login")
        base_currency = request.get("base_currency")
        amount = request.get("amount")
        microservice(
            "http://wallets/topup",
            {"login": login, "base_currency": base_currency, "amount": amount},
            "result"
        )

        return True

    @classmethod
    @cors
    @response_format
    def saveRate(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        base_currency = request.get("base_currency")
        value = request.get("value")
        datetime = request.get("datetime")
        return microservice(
            "http://converter/save",
            {"base_currency": base_currency, "value": value, "datetime": datetime},
            "result"
        )

    @classmethod
    @cors
    @response_format
    def saveRatesBulk(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        data = request.get("data")
        return microservice("http://converter/save_bulk", {"data": data}, "result")
