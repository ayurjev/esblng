"""
PUBLIC API

"""
from envi import Application
from controllers.auth.auth import AuthController

application = Application()

application.route("/auth/<action>/", AuthController)
