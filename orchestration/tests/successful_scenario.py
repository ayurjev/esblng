
from .utils import TestWrapper
from envi import microservice


class TestCase(TestWrapper):

    def test_one(self):
        print(microservice("http://public_api/getSupportedCurrencies", {}, "result"))