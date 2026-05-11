# Лабораторная работа 6

1. Собрать docker-образ:

```bash
docker build -t fast_api:latest .
```

2. Посмотреть список образов:

```bash
docker image list
```

3. Запустить контейнер:

```bash
docker run -d -p 9005:8000 -e DISABLE_DB=1 fast_api:latest
```

4. Открыть сервис:

```text
http://localhost:9005
```

5. Открыть Swagger:

```text
http://localhost:9005/docs
```

6. Посмотреть список контейнеров:

```bash
docker ps -a
```

7. Посмотреть лог контейнера:

```bash
docker logs <id контейнера>
```

8. Запустить вместе с PostgreSQL:

```bash
docker compose up --build
```

9. Остановить контейнеры:

```bash
docker compose down
```

10. Запустить тесты:

```bash
pytest -v
```
