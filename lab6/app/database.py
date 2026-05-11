import os
from datetime import datetime, timezone


_engine = None
_metadata = None
_predictions_table = None


def db_is_disabled() -> bool:
    return os.getenv("DISABLE_DB", "0") == "1"


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://mlops:mlops@db:5432/mlops_db",
    )


def get_engine():
    global _engine

    if db_is_disabled():
        return None

    if _engine is None:
        from sqlalchemy import create_engine

        _engine = create_engine(get_database_url(), pool_pre_ping=True)

    return _engine


def get_predictions_table():
    global _metadata, _predictions_table

    if _predictions_table is None:
        from sqlalchemy import Column, DateTime, Float, Integer, MetaData, String, Table

        _metadata = MetaData()
        _predictions_table = Table(
            "predictions",
            _metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("sepal_length", Float, nullable=False),
            Column("sepal_width", Float, nullable=False),
            Column("petal_length", Float, nullable=False),
            Column("petal_width", Float, nullable=False),
            Column("predicted_class", Integer, nullable=False),
            Column("predicted_name", String(64), nullable=False),
            Column("probability", Float, nullable=False),
            Column("created_at", DateTime(timezone=True), nullable=False),
        )

    return _metadata, _predictions_table


def init_db() -> None:
    if db_is_disabled():
        return

    engine = get_engine()
    metadata, _ = get_predictions_table()
    metadata.create_all(engine)


def save_prediction(features, prediction: dict) -> int | None:
    if db_is_disabled():
        return None

    engine = get_engine()
    _, table = get_predictions_table()

    stmt = (
        table.insert()
        .values(
            sepal_length=features.sepal_length,
            sepal_width=features.sepal_width,
            petal_length=features.petal_length,
            petal_width=features.petal_width,
            predicted_class=prediction["predicted_class"],
            predicted_name=prediction["predicted_name"],
            probability=prediction["probability"],
            created_at=datetime.now(timezone.utc),
        )
        .returning(table.c.id)
    )

    with engine.begin() as connection:
        return int(connection.execute(stmt).scalar_one())


def list_predictions(limit: int = 10) -> list[dict]:
    if db_is_disabled():
        return []

    from sqlalchemy import desc, select

    engine = get_engine()
    _, table = get_predictions_table()

    stmt = select(table).order_by(desc(table.c.id)).limit(limit)

    with engine.connect() as connection:
        rows = connection.execute(stmt).fetchall()

    return [dict(row._mapping) for row in rows]
