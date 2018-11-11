""" Exceptions """

from envi import BaseServiceException


class IncorrectLogin(BaseServiceException):
    """ Incorrect Login """
    code = "DC_AUTH_1"
    message = "Incorrect login"


class IncorrectPassword(BaseServiceException):
    """ Incorrect Password """
    code = "DC_AUTH_2"
    message = "Incorrect password"


class IncorrectToken(BaseServiceException):
    """ Incorrect Token """
    code = "DC_AUTH_3"
    message = "Incorrect token"


class AlreadyRegistred(BaseServiceException):
    """ Incorrect Token """
    code = "DC_AUTH_4"
    message = "Already registred"
