from envi import Controller, Request, microservice, response_format
from utils import cors


# noinspection PyPep8Naming,PyAbstractClass
class DefaultPublicController(Controller):

    @classmethod
    @cors
    @response_format
    def createAccount(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        login = request.get("login")
        password = request.get("password")
        name = request.get("name")
        country = request.get("country_id", request.get("country_name"))
        city = request.get("city_id", request.get("city_name"))
        base_currency = request.get("base_currency")

        microservice("http://auth/create", {"login": login, "password": password}, "result")

        country_id = microservice(
            "http://geo/get_country",
            {"id": country if country.isnumeric() else None, "name": country if not country.isnumeric() else None},
            "result.id"
        )

        city_id = microservice(
            "http://geo/get_city",
            {"id": city if city.isnumeric() else None, "name": city if not city.isnumeric() else None,
             "country_id": country_id},
            "result.id"
        )

        microservice(
            "http://users/create",
            {"login": login, "name": name, "country_id": country_id, "city_id": city_id},
            "result"
        )

        microservice(
            "http://wallets/create",
            {"login": login, "base_currency": base_currency},
            "result"
        )

        return True

    @classmethod
    @cors
    @response_format
    def auth(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        login = request.get("login")
        password = request.get("password")
        return microservice("http://auth/auth", {"login": login, "password": password}, "result")

    @classmethod
    @cors
    @response_format
    def getMe(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        token = request.get("token")
        login = microservice("http://auth/auth", {"token": token}, "result")
        wallets = microservice("http://wallets/get_wallets", {"login": login}, "result")
        user = microservice("http://users/get", {"login": login}, "result")
        user["country_name"] = microservice(
            "http://geo/get_country", {"id": user["country_id"]}, "result.name"
        )
        user["city_name"] = microservice(
            "http://geo/get_city", {"id": user["city_id"], "country_id": user["country_id"]}, "result.name"
        )
        return {**user, "wallets": wallets}

    @classmethod
    @cors
    @response_format
    def createWallet(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        token = request.get("token")
        login = microservice("http://auth/auth", {"token": token}, "result")
        base_currency = request.get("base_currency")
        return microservice(
            "http://wallets/create",
            {
                "login": login,
                "base_currency": base_currency
            },
            "result"
        )

    @classmethod
    @cors
    @response_format
    def getSupportedCurrencies(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        return microservice("http://wallets/get_currencies", {}, "result")

    @classmethod
    @cors
    @response_format
    def getConvertionRates(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        from_base_currency = request.get("from_base_currency")
        to_base_currency = request.get("to_base_currency")
        conversion_rate1 = microservice(
            "http://converter/get_last_value", {"base_currency": from_base_currency}, "result"
        )
        conversion_rate2 = microservice(
            "http://converter/get_last_value", {"base_currency": to_base_currency}, "result"
        )
        return {
            "conversion_rate1": conversion_rate1,
            "conversion_rate2": conversion_rate2
        }

    @classmethod
    @cors
    @response_format
    def transferMoney(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        token = request.get("token")
        login = microservice("http://auth/auth", {"token": token}, "result")
        from_base_currency = request.get("from_base_currency")

        to_login = request.get("to_login")
        to_base_currency = request.get("to_base_currency")

        amount = request.get("amount")
        conversion_rate_uuid_1 = request.get("conversion_rate_uuid_1", None)
        conversion_rate_uuid_2 = request.get("conversion_rate_uuid_2", None)

        return microservice(
            "http://wallets/transfer",
            {
                "from_login": login, "from_base_currency": from_base_currency,
                "to_login": to_login, "to_base_currency": to_base_currency,
                "amount": amount,
                "conversion_rate_uuid_1": conversion_rate_uuid_1,
                "conversion_rate_uuid_2": conversion_rate_uuid_2
            },
            "result"
        )