
from envi import BaseServiceException


class AccessDenied(BaseServiceException):
    """ AccessDenied  """
    code = "API_403"
    message = "Access Denied"

    def __init__(self, message=None):
        if message:
            self.message = AccessDenied.message + " (" + message + ")"
