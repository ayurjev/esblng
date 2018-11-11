
"""
Microservice `wallets`

User's wallet layer
"""

from envi import Application
from controllers import DefaultController

application = Application()
application.route("/<action>/", DefaultController)