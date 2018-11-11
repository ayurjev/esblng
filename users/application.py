
"""
Microservice `users`

Personal user's data layer
"""

from envi import Application
from controllers import DefaultController

application = Application()
application.route("/<action>/", DefaultController)