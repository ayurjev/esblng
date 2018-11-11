"""
PUBLIC API

"""
from envi import Application
from controllers import DefaultPublicController

application = Application()
application.route("/<action>/", DefaultPublicController)
