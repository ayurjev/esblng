

def cors(func):
    """ Декоратор для обработки любых исключений возникающих при работе сервиса
    :param func:
    """

    def wrapper(*args, **kwargs):
        """ wrapper
        :param args:
        :param kwargs:
        """
        request = kwargs.get("request")
        request.response.add_header('Access-Control-Allow-Origin', '*')
        request.response.add_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        request.response.add_header('Access-Control-Allow-Headers',
                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,'
                                    'Cache-Control,Content-Type,Content-Range,Range,token')
        request.response.add_header('Access-Control-Expose-Headers',
                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,'
                                    'Cache-Control,Content-Type,Content-Range,Range,token')
        return func(*args, **kwargs)

    return wrapper