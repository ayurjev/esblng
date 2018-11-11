
"""
Микросервис auth

Отвечает за слой аутентификации и регистрации
"""

from dc.envi import Application
from controllers import DefaultController

application = Application()
application.route("/<action>/", DefaultController)