
"""
Microservice `geo`

Geo layer (Cities and countries)
"""

from envi import Application
from controllers import DefaultController

application = Application()
application.route("/<action>/", DefaultController)