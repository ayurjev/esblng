
from dc.envi import microservice
from exceptions import AccessDenied


class AuthService(object):

    @staticmethod
    def auth(request):
        token = request.get("token", request.environ.get("HTTP_TOKEN", ""))
        login = request.get("login", None)
        password = request.get("password", None)
        try:
            user_id = microservice(
                "http://auth/authenticate",
                {
                    "login": login,
                    "password": password,
                    "token": token
                },
                "result.authentication.id"
            )
            user = microservice("http://users/get_user/", {"user_id": user_id}, "result")

        except Exception as e:
            raise AccessDenied(str(e))

        return user, user_id
