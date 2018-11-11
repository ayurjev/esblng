# Сборка и автоматические тесты:


После клонирования проекта необходимо перейти в каталог orchestration и запускать команды в следующем порядке:

Сборка базовых образов и запуск backend

```
./up_backend.sh
```

Сборка всех микросервисов, их запуск и запуск тестов всех микросервисов, которые их имеют

```
./unit_tests.sh
```

Подготовка к запуску оркестрации и интеграционных тестов

```
./up_all.sh
```


Запуск интеграционных тестов

```
./int_tests.sh
```


Остановить все приложение

```
./down.sh
```


# Документация по Public Api:

https://github.com/ayurjev/esblng/tree/master/public_api


# Документация по Private Api:

https://github.com/ayurjev/esblng/tree/master/private_api


# Прочитать интеграционный тест с комментариями:

https://github.com/ayurjev/esblng/blob/master/orchestration/tests/successful_scenario.py

