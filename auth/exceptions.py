
from envi import BaseServiceException


class IncorrectLogin(BaseServiceException):
    """ Incorrect Login """
    code = "AUTH_1"
    message = "Incorrect login"


class IncorrectPassword(BaseServiceException):
    """ Incorrect Password """
    code = "AUTH_2"
    message = "Incorrect password"


class IncorrectToken(BaseServiceException):
    """ Incorrect Token """
    code = "AUTH_3"
    message = "Incorrect token"


class AlreadyRegistred(BaseServiceException):
    """ Incorrect Token """
    code = "AUTH_4"
    message = "Already registred"
