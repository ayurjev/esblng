from dc.envi import Controller, Request, microservice, response_format
from models.Utils import cors


# noinspection PyPep8Naming,PyAbstractClass
class AuthController(Controller):

    @classmethod
    @cors
    @response_format(as_json=True)
    def create(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        login = request.get("login")
        password = request.get("password")
        return microservice("http://auth/create", {"login": login, "password": password}, "result")

    @classmethod
    @cors
    @response_format(as_json=True)
    def auth(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        token = request.get("token", None)
        login = request.get("login", None)
        password = request.get("password", None)
        return microservice("http://auth/auth", {"token": token, "login": login, "password": password}, "result")



