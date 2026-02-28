import os
import json
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import mlflow
from mlflow.models import infer_signature
import joblib


AIRFLOW_HOME = Path(os.environ.get("AIRFLOW_HOME", ".")).resolve()
DATA_DIR = AIRFLOW_HOME / "data" / "cars"
ARTIFACTS_DIR = AIRFLOW_HOME / "artifacts" / "cars"

DATA_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def scale_frame(frame: pd.DataFrame):
    df = frame.copy()
    X, y = df.drop(columns=["Price(euro)"]), df["Price(euro)"]

    scaler = StandardScaler()
    target_transformer = PowerTransformer()

    X_scaled = scaler.fit_transform(X.values)
    y_scaled = target_transformer.fit_transform(y.values.reshape(-1, 1))

    return X_scaled, y_scaled, scaler, target_transformer


def eval_metrics(actual, pred):
    rmse = float(np.sqrt(mean_squared_error(actual, pred)))
    mae = float(mean_absolute_error(actual, pred))
    r2 = float(r2_score(actual, pred))
    return rmse, mae, r2


def train():
    df_path = DATA_DIR / "df_clear.csv"
    df = pd.read_csv(df_path)

    X, y, scaler, target_transformer = scale_frame(df)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    params = {
        "alpha": [0.0001, 0.001, 0.01, 0.05, 0.1],
        "l1_ratio": [0.001, 0.01, 0.05, 0.2],
        "penalty": ["l1", "l2", "elasticnet"],
        "loss": ["squared_error", "huber", "epsilon_insensitive"],
        "fit_intercept": [False, True],
    }

    mlflow.set_tracking_uri(f"file://{(AIRFLOW_HOME / 'mlruns').as_posix()}")
    mlflow.set_experiment("linear model cars")

    with mlflow.start_run():
        base = SGDRegressor(random_state=42)
        clf = GridSearchCV(base, params, cv=3, n_jobs=1)
        clf.fit(X_train, y_train.reshape(-1))

        best = clf.best_estimator_

        y_pred_scaled = best.predict(X_val)
        y_pred_euro = target_transformer.inverse_transform(y_pred_scaled.reshape(-1, 1))
        y_val_euro = target_transformer.inverse_transform(y_val)

        rmse, mae, r2 = eval_metrics(y_val_euro, y_pred_euro)

        mlflow.log_params({
            "alpha": best.alpha,
            "l1_ratio": getattr(best, "l1_ratio", None),
            "penalty": best.penalty,
            "loss": best.loss,
            "fit_intercept": best.fit_intercept,
            "epsilon": getattr(best, "epsilon", None),
        })
        mlflow.log_metrics({"rmse": rmse, "mae": mae, "r2": r2})

        signature = infer_signature(X_train, best.predict(X_train))
        mlflow.sklearn.log_model(best, "model", signature=signature)

        model_path = ARTIFACTS_DIR / "best_model.joblib"
        scaler_path = ARTIFACTS_DIR / "scaler.joblib"
        target_tr_path = ARTIFACTS_DIR / "target_transformer.joblib"
        metrics_path = ARTIFACTS_DIR / "metrics.json"
        cv_path = ARTIFACTS_DIR / "cv_results.csv"

        joblib.dump(best, model_path)
        joblib.dump(scaler, scaler_path)
        joblib.dump(target_transformer, target_tr_path)

        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(
                {"rmse": rmse, "mae": mae, "r2": r2},
                f, ensure_ascii=False, indent=2
            )

        pd.DataFrame(clf.cv_results_).to_csv(cv_path, index=False)

        print(f"[OK] Saved model to: {model_path}")
        print(f"[OK] Saved metrics to: {metrics_path}")
        print(f"[OK] RMSE={rmse:.2f}  MAE={mae:.2f}  R2={r2:.3f}")

    return {"rmse": rmse, "mae": mae, "r2": r2}