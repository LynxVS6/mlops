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
DATA_DIR = AIRFLOW_HOME / "data" / "cars"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CARS_CSV = DATA_DIR / "cars.csv"
DF_CLEAR_CSV = DATA_DIR / "df_clear.csv"


def download_data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/dayekb/Basic_ML_Alg/main/cars_moldova_no_dup.csv",
        delimiter=",",
    )
    df.to_csv(CARS_CSV, index=False)
    print("Saved raw dataset to:", CARS_CSV)
    print("df shape:", df.shape)
    return True


def clear_data():
    df = pd.read_csv(CARS_CSV)

    cat_columns = ["Make", "Model", "Style", "Fuel_type", "Transmission"]

    # Очистка по здравому смыслу / выбросам
    question_dist = df[(df.Year < 2021) & (df.Distance < 1100)]
    df = df.drop(question_dist.index)

    question_dist = df[(df.Distance > 1e6)]
    df = df.drop(question_dist.index)

    question_engine = df[df["Engine_capacity(cm3)"] < 200]
    df = df.drop(question_engine.index)

    question_engine = df[df["Engine_capacity(cm3)"] > 5000]
    df = df.drop(question_engine.index)

    question_price = df[(df["Price(euro)"] < 101)]
    df = df.drop(question_price.index)

    question_price = df[df["Price(euro)"] > 1e5]
    df = df.drop(question_price.index)

    question_year = df[df.Year < 1971]
    df = df.drop(question_year.index)

    df = df.reset_index(drop=True)

    # Ordinal encoding категориальных колонок
    ordinal = OrdinalEncoder()
    df[cat_columns] = ordinal.fit_transform(df[cat_columns])

    # Сохраняем очищенный датасет
    df.to_csv(DF_CLEAR_CSV, index=False)
    print("Saved cleaned dataset to:", DF_CLEAR_CSV)
    print("df_clear shape:", df.shape)
    return True


dag_cars = DAG(
    dag_id="train_pipe",
    start_date=datetime(2025, 2, 3),
    schedule=timedelta(minutes=5),
    max_active_tasks=4,
    max_active_runs=1,
    catchup=False,
)

download_task = PythonOperator(
    task_id="download_cars",
    python_callable=download_data,
    dag=dag_cars,
)

clear_task = PythonOperator(
    task_id="clear_cars",
    python_callable=clear_data,
    dag=dag_cars,
)

train_task = PythonOperator(
    task_id="train_cars",
    python_callable=train,
    dag=dag_cars,
)

download_task >> clear_task >> train_task