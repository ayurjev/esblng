
PRIVATE API
=========================

>

Пополнение кошелька пользователя

```curl
curl -X POST \
  https://api.domain.com/topUpBalance/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F login=MyLogin \
  -F base_currency=1
  -F amount=100
```

200:
```json
{"result": true}
```

>

Получение истории транзакций кошелька пользователя

```curl
curl -X POST \
  https://api.domain.com/getTransactions/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F login=MyLogin \
  -F period_starts=Sun Nov 11 22:04:02 2018
  -F period_ends=Sun Nov 11 22:04:02 2018
```

200:
```json
{"result": {
    "incoming": [
        [tx_uuid, "MyLogin", Currencies.EUR, 2.0833, "USD-EUR-UUID", tx_datetime]
    ],
    "outgoing": [
        [tx_uuid, "MyLogin", Currencies.CNY, 10.0, "CNY-USD-UUID", tx_datetime]
    ]
}}
```

>


Получение истории транзакций кошелька пользователя в формате файла csv

```curl
curl -X POST \
  https://api.domain.com/getTransactionsCsvReport/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F login=MyLogin \
  -F period_starts=Sun Nov 11 22:04:02 2018
  -F period_ends=Sun Nov 11 22:04:02 2018
```

200:
```
 -H 'content-type: application/vnd.ms-excel'
 -H 'content-disposition: attachment; filename=transactions-MyLogin.csv'
```

>

Сохранение котировки валюты на момент времени (одиночная операция)

```curl
curl -X POST \
  https://api.domain.com/saveRate/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F base_currency=1
  -F value=1.42
  -F datetime=Sun Nov 11 22:04:02 2018
```

200:
```json
{"result": true}
```

>

Сохранение котировок валют на момент времени (bulk-mode)

```curl
curl -X POST \
  https://api.domain.com/saveRate/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{"data": [{"base_currency": 1, "value": 1.42, "datetime": "Sun Nov 11 22:04:02 2018"}]}'
```

200:
```json
{"result": true}
```