
from envi import Controller, Request, response_format
from models import ClickHouse


# noinspection PyAbstractClass
class DefaultController(Controller):

    @classmethod
    @response_format
    def save(cls, request: Request, **kwargs):
        """ Saving rates """
        base_currency = request.get("base_currency")
        value = request.get("value")
        datetime = request.get("datetime", None)
        return ClickHouse.save(base_currency, value, datetime)

    @classmethod
    @response_format
    def save_bulk(cls, request: Request, **kwargs):
        """ Saving rates (BULK-mode) """
        data = request.get("data", [])
        return ClickHouse.save_bulk(data)

    @classmethod
    @response_format
    def get_last_value(cls, request: Request, **kwargs):
        """ Retrieving last known convertion rate for the currency """
        base_currency = request.get("base_currency")
        return ClickHouse.get_last_value(base_currency)

    @classmethod
    @response_format
    def get_by_uuid(cls, request: Request, **kwargs):
        """ Retrieving convertion rate for the currency by its id """
        uuid = request.get("uuid")
        return ClickHouse.get_by_uuid(uuid)
