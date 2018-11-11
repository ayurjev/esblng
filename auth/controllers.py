
from envi import Controller, Request, response_format
from models import CredentialsRecords


# noinspection PyAbstractClass
class DefaultController(Controller):

    @classmethod
    @response_format
    def create(cls, request: Request, **kwargs):
        """ Creating new account """
        login = request.get("login")
        password = request.get("password")
        return CredentialsRecords.create_new(login, password)

    @classmethod
    @response_format
    def auth(cls, request: Request, **kwargs):
        """ Authenticating """
        token = request.get("token", None)
        if token:
            return CredentialsRecords.auth_by_token(token)
        else:
            login = request.get("login")
            password = request.get("password")
            return CredentialsRecords.auth(login, password)
