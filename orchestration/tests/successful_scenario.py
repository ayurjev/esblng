
from datetime import datetime
from .utils import TestWrapper
from envi import microservice


class TestCase(TestWrapper):

    def test_successfull_scenario(self):
        """ Lets test successfull sceanrio of using the app """

        # Registration:
        registration_result = microservice(
            "http://public_api/createAccount",
            {
                "login": "MyLogin", "password": "MyPassword", "name": "Andrey",
                "country_name": "Russia", "city_name": "Moscow",
                "base_currency": 1
            },
            "result"
        )
        self.assertTrue(registration_result)

        # Authenticatation:
        token = microservice(
            "http://public_api/auth",
            {"login": "MyLogin", "password": "MyPassword"},
            "result"
        )

        # Getting user data back, including list of wallets:
        user_data = microservice("http://public_api/getMe", {"token": token}, "result")
        self.assertDictEqual(
            {
                "city_id": 1,                           # Here we can see that our geo-info now have ids,
                "city_name": "Moscow",                  # so it could be reused by other users
                "country_id": 1,                        # with some help from the front-end
                "country_name": "Russia",
                "login": "MyLogin",
                "name": "Andrey",
                # Also we have our first wallet for USD right after registration:
                "wallets": [{"balance": 0.0, "base_currency": 1, "login": "MyLogin"}]},
            user_data
        )

        # Let's try to create another wallet for different currency...
        # First of all, we need to know what currencies are currently supported by the platform:
        supported_currencies = microservice(
            "http://public_api/getSupportedCurrencies", {}, "result"
        )
        self.assertDictEqual(
            {"1": "USD", "2": "EUR", "3": "CAD", "4": "CNY"},
            supported_currencies
        )

        # We already have a USD-wallet, so let's create CNY:
        new_wallet_creation = microservice(
            "http://public_api/createWallet", {"token": token, "base_currency": 4}, "result"
        )
        self.assertTrue(new_wallet_creation)

        #Let's check our wallets now:
        user_wallets = microservice("http://public_api/getMe", {"token": token}, "result.wallets")
        self.assertEqual(
            [
                {"balance": 0.0, "base_currency": 1, "login": "MyLogin"},
                {"balance": 0.0, "base_currency": 4, "login": "MyLogin"}
            ],
            user_wallets
        )

        # Ok, so far so good...
        # But to test further we need to get some money into one of our wallets...
        # We can do that by using private_api, that should be only accessible for trusted persons:
        topping_up_result = microservice(
            "http://private_api/topUpBalance", {"login": "MyLogin", "base_currency": 1, "amount": 100}, "result"
        )
        self.assertTrue(topping_up_result)

        # Have we become a millionaires already? Lets find out:
        user_wallets = microservice("http://public_api/getMe", {"token": token}, "result.wallets")
        self.assertEqual(
            [
                {"balance": 100.0, "base_currency": 1, "login": "MyLogin"},
                {"balance": 0.0, "base_currency": 4, "login": "MyLogin"}
            ],
            user_wallets
        )

        # Awesome!!! 100$!!! =)
        # We need CNY for travelling though... no problem - using public api again we can make a transfer:

        # But wait the minute... our platform doesn't know anything about current convertion rates yet...
        # Let's fix this via our private-api too:
        update_dt = datetime.now().strftime("%c")
        updating_convertion_rates = microservice(
            "http://private_api/saveRatesBulk",
            {"data": [
                {"base_currency": 2, "value": 1.24, "datetime": update_dt},    # 1EUR = 1.24USD
                {"base_currency": 4, "value": 0.25, "datetime": update_dt},    # 1CNY = 0.25USD
            ]},
            "result"
        )
        self.assertTrue(updating_convertion_rates)

        # And now, as user, we need to know current convertion rates and see if it works for us:
        # We are going to transfer USD to CNY, so:
        convertion_rates = microservice(
            "http://public_api/getConvertionRates",
            {
                "token": token,
                "from_base_currency": 1,
                "to_base_currency": 4,
            },
            "result"
        )

        cny_uuid = convertion_rates["conversion_rate2"]["uuid"]
        self.assertDictEqual(
            {
                "conversion_rate1": {"uuid": None, "value": 1, "datetime": None, "base_currency": 1},
                "conversion_rate2": {"uuid": cny_uuid, "value": 0.25, "datetime": update_dt, "base_currency": 4}
            },
            convertion_rates
        )

        # I hope that front-end will represent this information in a more understandable way... =)

        # But, let's make our transfer already!
        transfer_result = microservice(
            "http://public_api/transferMoney",
            {
                "token": token,
                "from_base_currency": 1,
                "to_login": "MyLogin",
                "to_base_currency": 4,
                "amount": 100,
                "conversion_rate_uuid_1": None,
                "conversion_rate_uuid_2": cny_uuid      # this is important, this should not be too old (< 30 seconds)
            },
            "result"
        )
        self.assertTrue(transfer_result)

        # Final checking:
        user_wallets = microservice("http://public_api/getMe", {"token": token}, "result.wallets")
        self.assertEqual(
            [
                {"balance": 0.0, "base_currency": 1, "login": "MyLogin"},
                {"balance": 400.0, "base_currency": 4, "login": "MyLogin"}
            ],
            user_wallets
        )

        # Profit! =)
