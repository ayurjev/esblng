""" Exceptions """

from envi import BaseServiceException


class CommonException(BaseServiceException):
    """ CommonException """
    code = "USERS_1"
    message = "USERS_1"