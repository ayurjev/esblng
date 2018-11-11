""" Exceptions """

from envi import BaseServiceException


class CountryNotFound(BaseServiceException):
    """ CountryNotFound """
    code = "GEO_1"
    message = "Unknown country"


class CityNotFound(BaseServiceException):
    """ CityNotFound """
    code = "GEO_2"
    message = "Unknown city"