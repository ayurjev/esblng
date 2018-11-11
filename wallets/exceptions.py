
from envi import BaseServiceException


class UnsupportedCurrency(BaseServiceException):
    """ UnsupportedCurrency """
    code = "WALLETS_1"
    message = "Unsupported Currency"

class WalletNotFound(BaseServiceException):
    """ WalletNotFound """
    code = "WALLETS_2"
    message = "Wallet Not Found"


class InsufficientFunds(BaseServiceException):
    """ InsufficientFunds """
    code = "WALLETS_3"
    message = "Insufficient Funds"


class NoConversionRateProvided(BaseServiceException):
    """ NoConversionRateProvided """
    code = "WALLETS_4"
    message = "No Conversion Rate uuid Provided"


class ConvertionRateExpired(BaseServiceException):
    """ ConvertionRateExpired """
    code = "WALLETS_5"
    message = "Convertion Rate Expired"


class InvalidConvertionRate(BaseServiceException):
    """ InvalidConvertionRate """
    code = "WALLETS_6"
    message = "Invalid Convertion Rate"

