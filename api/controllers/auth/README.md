
Auth API
=========================

>

Создание новой учетной записи

```curl
curl -X POST \
  https://api.domain.com/auth/create/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F login=MyLogin \
  -F password=MyPassword
```

200:
```json
{"result": true}
```


>

Аутентификация

```curl
curl -X POST \
  https://api.domain.com/auth/auth/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F login=MyLogin \
  -F password=MyPassword
```

200:
```json
{"result": "9a1c43b6-8e1a-cfcd-7798-34b33e9a52fd"}
```