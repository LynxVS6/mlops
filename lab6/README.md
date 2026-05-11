# Лабораторная работа 6

1. Запустить приложение и базу данных:

```bash
docker compose up --build
```

2. Открыть сервис:

```text
http://localhost:8000
```

3. Открыть Swagger:

```text
http://localhost:8000/docs
```

4. Посмотреть контейнеры:

```bash
docker ps -a
```

Должны быть контейнеры:

```text
mlops_fastapi_api
mlops_fastapi_db
```

5. Посмотреть логи приложения:

```bash
docker logs mlops_fastapi_api
```

6. Посмотреть логи базы:

```bash
docker logs mlops_fastapi_db
```

7. Остановить контейнеры:

```bash
docker compose down
```

8. Установить библиотеки:

```bash
python -m pip install -r requirements.txt
```

9. Запустить тесты:

```bash
pytest -v
```

10. Если нужно запустить только приложение без базы:

```bash
docker build -t fast_api:latest .
docker run -d --name lab6_api -p 9005:8000 -e DISABLE_DB=1 fast_api:latest
```

Тогда сервис будет доступен по адресу:

```text
http://localhost:9005
```
