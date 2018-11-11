
import io
import csv
from datetime import datetime
from envi import Controller, Request, microservice, response_format
from utils import cors


# noinspection PyPep8Naming,PyAbstractClass
class DefaultPrivateController(Controller):

    @classmethod
    @cors
    @response_format
    def topUpBalance(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        login = request.get("login")
        base_currency = request.get("base_currency")
        amount = request.get("amount")
        microservice(
            "http://wallets/topup",
            {"login": login, "base_currency": base_currency, "amount": amount},
            "result"
        )

        return True

    @classmethod
    @cors
    @response_format
    def getTransactions(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        login = request.get("login")
        period_starts = request.get("period_starts", None)
        period_ends = request.get("period_ends", None)
        return microservice(
            "http://wallets/get_transactions",
            {"login": login, "period_starts": period_starts, "period_ends": period_ends},
            "result"
        )

    @classmethod
    @cors
    def getTransactionsCsvReport(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        login = request.get("login")
        period_starts = request.get("period_starts", None)
        period_ends = request.get("period_ends", None)
        transactions = microservice(
            "http://wallets/get_transactions",
            {"login": login, "period_starts": period_starts, "period_ends": period_ends},
            "result"
        )
        all_transactions = [tx + ["+"] for tx in transactions["incoming"]] + \
                           [tx + ["-"] for tx in transactions["outgoing"]]
        all_transactions.sort(key=lambda tx: datetime.strptime(tx[5], "%c"))

        csv_header = ["tx_uuid", "login", "base_currency", "amount", "convertion_rate_uuid", "tx_datetime", "mode"]
        csv_body = [csv_header]

        for tx in all_transactions:
            csv_body.append(tx)

        file = io.StringIO()
        writer = csv.writer(file, delimiter=",")
        writer.writerows(csv_body)
        result = file.getvalue()

        request.response.add_header("Content-Type", 'application/vnd.ms-excel')
        request.response.add_header("Content-disposition", 'attachment; filename=transactions-%s.csv' % login)
        return result

    @classmethod
    @cors
    @response_format
    def saveRate(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        base_currency = request.get("base_currency")
        value = request.get("value")
        datetime = request.get("datetime")
        return microservice(
            "http://converter/save",
            {"base_currency": base_currency, "value": value, "datetime": datetime},
            "result"
        )

    @classmethod
    @cors
    @response_format
    def saveRatesBulk(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        data = request.get("data")
        return microservice("http://converter/save_bulk", {"data": data}, "result")
