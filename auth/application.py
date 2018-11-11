
"""
Microservice `auth`

Registration and authentication layer
"""

from dc.envi import Application
from controllers import DefaultController

application = Application()
application.route("/<action>/", DefaultController)