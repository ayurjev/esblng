
from envi import BaseServiceException


class UnknownRatesInformation(BaseServiceException):
    """ UnknownRatesInformation """
    code = "CONVERTER_1"
    message = "No Data For Requested Currency"
