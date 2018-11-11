
Auth API
=========================

>

Создание новой учетной записи

```curl
curl -X POST \
  https://api.domain.com/createAccount \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F login=MyLogin \
  -F password=MyPassword
  -F name=MyName
  -F country_id=1
  -F country_name="Russia"
  -F city_id=1
  -F city_name="Moscow"
  -F base_currency=1
```

200:
```json
{"result": true}
```


>

Аутентификация

```curl
curl -X POST \
  https://api.domain.com/auth/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F login=MyLogin \
  -F password=MyPassword
```

200:
```json
{"result": "9a1c43b6-8e1a-cfcd-7798-34b33e9a52fd"}
```


>

Получение данных авторизованного пользователя

```curl
curl -X POST \
  https://api.domain.com/auth/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F token=9a1c43b6-8e1a-cfcd-7798-34b33e9a52fd
```

200:
```json
{"result": {
    "login": "MyLogin", "name": "MyName", "country_id": 1, "country_name": "Russia", "city_id": 2, "city_name": "Moscow",
    "wallets": [
        {"login": "MyLogin", "base_currency": 1, "balance": 0.0}
    ]
}}
```


>

Создание нового кошелька пользователя

```curl
curl -X POST \
  https://api.domain.com/createWallet/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F token=9a1c43b6-8e1a-cfcd-7798-34b33e9a52fd
  -F base_currency=2
```

200:
```json
{"result": true}
```

>

Получение списка поддерживаемых валют

```curl
curl -X POST \
  https://api.domain.com/getSupportedCurrencies/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F token=9a1c43b6-8e1a-cfcd-7798-34b33e9a52fd
  -F base_currency=2
```

200:
```json
{"result": {1: "USD", 2: "EUR", 3: "CAD", 4: "CNY"}}
```

>

Получение идентификаторов обменных курсов, необходимых для осуществления перевода

```curl
curl -X POST \
  https://api.domain.com/getConvertionRates/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F token=9a1c43b6-8e1a-cfcd-7798-34b33e9a52fd
  -F from_base_currency=1
  -F to_base_currency=2
```

200:
```json
{"result": {
    "conversion_rate1": {"uuid": "576ff813-d370-475d-aa02-c576ef291b96", "value": 1.21, "datetime": "Sun Nov 11 22:04:02 2018", "base_currency": 1},
    "conversion_rate2": {"uuid": "576ff813-d370-475d-aa02-c576ef291b96", "value": 2.45, "datetime": "Sun Nov 11 22:04:02 2018", "base_currency": 2}
}}
```

>

Перевод средств с одного кошелька на другой

```curl
curl -X POST \
  https://api.domain.com/transferMoney/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F token=9a1c43b6-8e1a-cfcd-7798-34b33e9a52fd
  -F from_base_currency=1
  -F to_login="ReceiverLogin"
  -F to_base_currency=2
  -F amount=100
  -F conversion_rate_uuid_1=null
  -F conversion_rate_uuid_2=576ff813-d370-475d-aa02-c576ef291b96
```

200:
```json
{"result": {
    "conversion_rate1": {"uuid": "576ff813-d370-475d-aa02-c576ef291b96", "value": 1.21, "datetime": "Sun Nov 11 22:04:02 2018", "base_currency": 1},
    "conversion_rate2": {"uuid": "576ff813-d370-475d-aa02-c576ef291b96", "value": 2.45, "datetime": "Sun Nov 11 22:04:02 2018", "base_currency": 2}
}}
```

getConvertionRates