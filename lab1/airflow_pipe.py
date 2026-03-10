from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

from airflow import DAG
from airflow.operators.python import PythonOperator

from train_model import train


AIRFLOW_HOME = Path(os.environ.get("AIRFLOW_HOME", ".")).resolve()
DATA_DIR = AIRFLOW_HOME / "data" / "food"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FOOD_CSV = DATA_DIR / "food.csv"
DF_CLEAR_CSV = DATA_DIR / "df_clear.csv"

DATA_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-09-04/fastfood_calories.csv"


def download_data():
    df = pd.read_csv(DATA_URL, delimiter=",")

    df.columns = [
        c.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
        for c in df.columns
    ]

    df.to_csv(FOOD_CSV, index=False)
    print("Saved raw dataset to:", FOOD_CSV)
    print("df shape:", df.shape)
    return True


def clear_data():
    df = pd.read_csv(FOOD_CSV)

    if "item" in df.columns:
        df = df.drop(columns=["item"])

    cat_columns = [col for col in ["restaurant", "salad"] if col in df.columns]

    for col in df.columns:
        if col not in cat_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates()

    if "calories" in df.columns:
        df = df.dropna(subset=["calories"])
        df = df[(df["calories"] > 0) & (df["calories"] < 3000)]

    for col in df.columns:
        if col not in cat_columns and col != "calories":
            df[col] = df[col].fillna(df[col].median())

    if "sodium" in df.columns:
        df = df[df["sodium"] < 10000]

    if "protein" in df.columns:
        df = df[df["protein"] < 200]

    if "total_fat" in df.columns:
        df = df[df["total_fat"] < 200]

    if "total_carb" in df.columns:
        df = df[df["total_carb"] < 300]

    df = df.reset_index(drop=True)

    for col in cat_columns:
        df[col] = df[col].fillna("unknown").astype(str)

    if cat_columns:
        ordinal = OrdinalEncoder()
        df[cat_columns] = ordinal.fit_transform(df[cat_columns])

    df.to_csv(DF_CLEAR_CSV, index=False)
    print("Saved cleaned dataset to:", DF_CLEAR_CSV)
    print("df_clear shape:", df.shape)
    return True


dag_food = DAG(
    dag_id="train_food_pipe",
    start_date=datetime(2025, 2, 3),
    max_active_tasks=4,
    schedule=timedelta(minutes=5),
    max_active_runs=1,
    catchup=False,
)

download_task = PythonOperator(
    python_callable=download_data,
    task_id="download_food",
    dag=dag_food,
)

clear_task = PythonOperator(
    python_callable=clear_data,
    task_id="clear_food",
    dag=dag_food,
)

train_task = PythonOperator(
    python_callable=train,
    task_id="train_food",
    dag=dag_food,
)

download_task >> clear_task >> train_task
