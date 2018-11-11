
from envi import BaseServiceException


class UnsupportedCurrency(BaseServiceException):
    """ UnsupportedCurrency """
    code = "WALLETS_1"
    message = "Unsupported Currency"