
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