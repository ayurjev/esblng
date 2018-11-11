
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