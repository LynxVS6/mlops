# Лабораторная работа MLOps: FastAPI + ML model + Docker + PostgreSQL + pytest

## Что сделано

В проекте реализован web-сервис на FastAPI, который оборачивает ML-модель классификации ирисов.

Сервис принимает признаки цветка:

- `sepal_length`
- `sepal_width`
- `petal_length`
- `petal_width`

И возвращает:

- номер предсказанного класса
- название класса
- вероятность предсказания
- id сохраненной записи в базе данных

Дополнительно используется PostgreSQL в отдельном контейнере через `docker-compose`.
Каждый запрос к `/predict` сохраняется в таблицу `predictions`.

## Структура проекта

```text
mlops_fastapi_lab/
├── app/
│   ├── __init__.py
│   ├── database.py       # подключение к PostgreSQL и сохранение предсказаний
│   ├── main.py           # FastAPI-приложение
│   ├── model.py          # загрузка, обучение и использование модели
│   └── schemas.py        # Pydantic-схемы запросов и ответов
├── models/               # сюда сохраняется model.joblib
├── tests/
│   ├── test_api.py       # тесты API
│   └── test_model.py     # тесты модели
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── train_model.py
└── README.md
```

## Локальный запуск без Docker

Создать виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Обучить и сохранить модель:

```bash
python train_model.py
```

Запустить сервис локально:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Открыть Swagger UI:

```text
http://localhost:8000/docs
```

## Запуск через Docker Compose

Собрать и запустить сервис вместе с PostgreSQL:

```bash
docker compose up --build
```

После запуска будут подняты 2 контейнера:

- `mlops_fastapi_api` — FastAPI-приложение
- `mlops_fastapi_db` — PostgreSQL база данных

Открыть приложение:

```text
http://localhost:8000
```

Открыть Swagger UI:

```text
http://localhost:8000/docs
```

## Проверка API через curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

Пример ответа:

```json
{
  "predicted_class": 0,
  "predicted_name": "setosa",
  "probability": 1.0,
  "saved_id": 1
}
```

Посмотреть историю предсказаний:

```bash
curl "http://localhost:8000/history"
```

## Запуск тестов

Тесты проверяют:

- что модель загружается
- что модель корректно предсказывает классы на известных примерах
- что endpoint `/predict` работает
- что FastAPI возвращает ошибку валидации на некорректные данные

Запуск:

```bash
pytest -v
```

В тестах база данных отключается через переменную:

```python
os.environ["DISABLE_DB"] = "1"
```

Это сделано потому, что по заданию pytest должен проверять модель, а PostgreSQL используется при запуске приложения через `docker-compose`.

## Полезные Docker-команды

Посмотреть контейнеры:

```bash
docker ps -a
```

Посмотреть логи API:

```bash
docker logs mlops_fastapi_api
```

Посмотреть логи базы данных:

```bash
docker logs mlops_fastapi_db
```

Остановить контейнеры:

```bash
docker compose down
```

Остановить контейнеры и удалить volume с данными PostgreSQL:

```bash
docker compose down -v
```

## Что можно показать преподавателю

1. Структуру проекта
2. `Dockerfile`
3. `docker-compose.yml`
4. Запуск `docker compose up --build`
5. Swagger UI по адресу `http://localhost:8000/docs`
6. POST-запрос на `/predict`
7. GET-запрос на `/history`
8. Запуск `pytest -v`
9. Два контейнера: FastAPI и PostgreSQL
