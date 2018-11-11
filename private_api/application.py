"""
PRIVATE API

"""
from envi import Application
from controllers import DefaultPrivateController

application = Application()
application.route("/<action>/", DefaultPrivateController)
