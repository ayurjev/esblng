
"""
Microservice `converter`

Currencies and convertion rates
"""

from envi import Application
from controllers import DefaultController

application = Application()
application.route("/<action>/", DefaultController)