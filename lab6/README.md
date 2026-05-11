# Лабораторная работа 6

1. Перейти в папку лабораторной:

```bash
cd lab6
```

2. Запустить приложение и базу данных:

```bash
docker compose up --build
```

3. Открыть сервис:

```text
http://localhost:8000
```

4. Открыть Swagger:

```text
http://localhost:8000/docs
```

5. Посмотреть контейнеры:

```bash
docker ps -a
```

Должны быть контейнеры:

```text
mlops_fastapi_api
mlops_fastapi_db
```

6. Посмотреть логи приложения:

```bash
docker logs mlops_fastapi_api
```

7. Посмотреть логи базы:

```bash
docker logs mlops_fastapi_db
```

8. Остановить контейнеры:

```bash
docker compose down
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
